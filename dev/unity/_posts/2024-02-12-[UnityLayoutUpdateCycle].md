---
layout: single
title: "Unity GUI 의 Layout Update Cycle - soo:bak"
date: "2024-02-13 21:03:00 +0900"
---
<br>

`Unity GUI` 시스템의 `Layout Update Cycle` 은 `UI` 요소들의 위치, 크기 및 다른 `Layout` 관련 속성들을 계산하고 적용하는 과정을 말한다.<br>
<br>
각각 단계는 `UI` 의 동적 반응성을 가능하게 하며, 다양한 화면 크기와 해상도 등에 적절히 대응할 수 있도록 한다.<br>
<br>
이번 포스팅에서는 `Unity GUI` 시스템의 `Layout Update Cycle` 을 자세히 살펴봄을 통해, `UI` 요소들의 `Layout` 이 어떻게 갱신되는지 다뤄보고자 한다.<br>
<br>
<br>
> Unity 의 UI 시스템인, UGUI(Unity GUI)의 Update Cycle 은, Unity 의 표준 생명주기 이벤트와 연결되어 있지만, 정확하게 일치하지는 않는다.<br>
<br>
즉, UGUI 의 Update 와 Rendering 은 Unity의 표준 생명 주기 사이 사이에서 처리된다.<br>
<br>
이 때, UGUI 의 Update Cycle 중 Layout Update Cycle(해당 포스트 주제), Graphic Update 는 Unity 의 표준 생명 주기 중, Update 단계 '이전' 에 발생한다.<br>
<br>
<br>
반면, UGUI 의 Rendering 은 Unity 의 표준 생명 주기 중 LateUpdate 단계 '이후' 에 발생한다.<br>
<br>
이 때, 모든 Layout 및 Graphic Update 가 반영된 상태에서 UI 요소들이 최종적으로 화면에 렌더링되게 된다.<br>
<br>
이는, UI 요소들이 Update 단계에서 사용자의 입력에 반응할 수 있도록 하고, 관련 로직이 처리된 후 시각적 요소들을 최신 상태로 갱신하기 위함이다.<br>

<br>
<br>
<br>
<br>

## 레이아웃 업데이트 사이클(Layout Update Cycle)
`Layout Update Cycle` 은 `Unity GUI` 시스템이 '`UI` 요소들의 `Layout` 과 `Rendering` 을 어떻게 처리하는지' 에 대한 전체적인 흐름을 나타낸다.<br>
<br>
각 단계는 다음과 같은 과정으로 나뉜다.<br>
<br>
<br>
- Rebuild Phase<br>
<br>
- Pre-Rebuild Layout Phase<br>
<br>
- Calculation Phase<br>
<br>
- Set Layout Phase<br>
<br>
- Finalization Phase<br>
<br>
- Rendering Phase<br>
<br>
<br>
<br>
<br>

## Rebuild Phase
이 단계는 `Unity GUI` 시스템 내에서 `UI` 요소들이 변화할 때, 그에 대응하여 `Layout system` 이 적절하게 반응하도록 하는 단계이다.<br>
<br>
즉, `UI` 의 동적인 변화를 실시간으로 반영하며, `UI` 가 사용자와의 상호작용에 빠르게 대응할 수 있도록 한다.<br>
<br>
`Rebuild Phase` 의 역할은 '변화 감지' 라고도 할 수 있다.<br>
<br>
`Unity GUI` 시스템은 `RectTransform` 의 속성 변경(예: 크기, 위치), `UI` 요소의 활성화/비활성화 등의 이벤트를 <b>지속적으로 모니터링</b>한다.<br>
<br>
이러한 변화는 `UI` 요소들의 시각적 표현이나 레이아웃에 직접적인 영향을 미칠 수 있기 때문에, 시스템은 이를 감지하는 즉시 반응해야 하기 때문이다.<br>
<br>
<br>
<br>

### 연관 컴포넌트
`Rebuild Phase` 와 연관된 컴포넌트는 다음과 같다.<br>
<br>

<b>Canvas</b><br>
<br>: `Canvas` 컴포넌트는 `UI` 요소들이 그려지는 <b>'화면'</b>을 제공하며, `UI` 요소들의 레이아웃과 렌더링을 총괄한다.<br>
<br>
`Canvas` 내부에서 발생하는 모든 변화는 `Canvas` 컴포넌트에 의해서 관리되며, 필요한 경우 레이아웃 시스템에 재계산이 필요함을 알린다.<br>
<br>

<b>LayoutRebuilder</b><br>
<br>: `LayoutRebuilder` 클래스는 레이아웃의 재계산과 관련된 <u>명시적인 작업</u>을 수행하는 역할을 담당한다.<br>
<br>
즉, 개발자로 하여금 특정 `UI` 요소에 대한 레이아웃 재계산을 직접 요청할 수 있게 해주는 `API` 를 제공한다.<br>
<br>
- LayoutRebuilder 의 주요 API<br>
  <br>
  - `MarkLayoutForRebuild(RectTransfrom rectTransform)`<br>
    <br>: 이 메서드는 지정된 `RectTransform` 에 대해 레이아웃을 재계산하도록 시스템에 요청한다.<br>
    <br>
    이 때, `RectTransfrom` 이 일명 `"dirty"` 상태로 표시되며, 다음 레이아웃 업데이트 사이클에서 재계산이 수행되도록 한다.<br>
    <br>
  - `Rebuild(CanvasUpdate executing)`<br>
    <br>: `CanvasUpdate` 열거형을 매개변수로 받아, 지정된 업데이트 단계에서 레이아웃 재계산을 수행한다.<br>
    <br>
    `CanvasUpdate.Layout` 과 `CanvasUpdate.GraphicUpdate` 단계에서 사용될 수 있다.<br>
  - `ForeRebuildLayoutImmediate(RectTransfrom layoutRoot)`<br>
    <br>: 이 메서드는 지정된 `RectTransform` 의 레이아웃을 즉시 재계산하고 적용한다.<br>
    <br>
    즉, 레이아웃 변경이 즉각적으로 반영되어야 할 경우에 유용하게 사용된다.<br>
<br>

`LayoutRebuilder` 는 `Unity GUI` 시스템의 레이아웃 업데이트 메커니즘과 밀접하게 연동되어 작동하는데,<br>
<br>
`MarkLayoutForRebuild` 메서드를 통해 `"dirty"` 상태로 표시된 `RectTransform` 은 `Unity` 의 <b>내부 레이아웃 업데이트 큐</b>에 추가된다.<br>
<br>
`Unity GUI` 시스템은 프레임의 레이아웃 업데이트 단계에서 이 큐를 처리하며, 큐에 있는 모든 `UI` 요소들에 대해 레이아웃을 재계산하고 적용한다.<br>
<br>

즉, `LayoutRebuilder` 의 사용은 동적인 `UI` 요소들의 레이아웃을 프로그래밍적으로 제어할 필요가 있을 때 유용하다.<br>
<br>
예를 들어, 동적으로 콘텐츠가 추가되거나 제거될 때, `UI` 요소의 레이아웃을 즉각적으로 업데이트하기 위해 사용할 수 있다.<br>
<br>
<br>
<br>

### 작동 방식
`LayoutRebuilder` 의 핵심 메서드는, '레이아웃 재계산 과정을 직접적으로 촉발시키는' `MarkLayoutForRebuild(RectTransform)` 메서드 이다.<br>
<br>
해당 메서드를 통한 레이아웃 재계산 과정을 살펴보면 다음과 같다.<br>
<br>
<br>

1. 메서드 호출<br>
<br>: `RectTransform` 의 변화에 대응하거나, 특정 `UI` 요소의 레이아웃을 명시적으로 갱신하고자 할 때, `LayoutRebuilder.MarkLayoutForRebuild` 메서드를 호출한다.<br>
<br>
<br>

2. `"Dirty"` 상태 설정<br>
<br>: 호출된 `RectTransform` 은 일명 `"dirty"` 상태로 표시된다.<br>
<br>
이는 해당 `UI` 요소의 레이아웃이 변경되었으며, 레이아웃 시스템은 이를 재계산해야 함을 의미한다.<br>
<br>

3. 레이아웃 큐에 추가<br>
<br>: `"dirty"` 상태로 표시된 `RectTransform` 은 레이아웃 재계산을 위한 큐에 추가된다.<br>
<br>
`Unity GUI` 시스템은 이 큐를 관리하며, 적절한 시점에 큐에 있는 모든 `UI` 요소들에 대해 레이아웃을 재계산한다.<br>
<br>

4. 재계산 실행<br>
<br>: 레이아웃 시스템은 큐에 있는 모든 `"dirty"` `UI` 요소들에 대하여 레이아웃 재계산을 수행한다.<br>
<br>
이 과정에서 `ILayoutElement` 와 `ILayoutController` 인터페이스를 구현하는 컴포넌트들이 레이아웃 계산과 적용 과정에 참여한다.<br>
<br>

- `ILayoutElement` 를 구현하는 컴포넌트<br>
  - `LayoutElement`<br>
   <br>: 개별 `UI` 요소에 대한 최소 크기, 선호 크기 등을 명시적으로 설정할 수 있도록 한다.<br>
   <br>
   이를 통해 레이아웃 시스템이 해당 `UI` 요소를 어떻게 배치하고 크기를 조정할지 결정할 수 있다.<br>
   <br>
   - `ContentSizeFitter` (`ILayoutController` 또한 구현)<br>
   <br>: 자식 요소들의 콘텐츠 크기에 기반하여 `UI` 요소의 크기를 조정한다.<br>
   `ILayoutElement` 인터페이스를 구현하여, 콘텐츠 크기에 따른 최소 크기와 선호 크기를 레이아웃 시스템에 제공한다.<br>
   <br>
   - `Text`, `Image`, `RawImage`<br>
   <br>: 이들 모두 `ILayoutElement` 인터페이스를 구현하며, 해당 컴포넌트의 내용이 차지하는 크기를 레이아웃 시스템에 제공한다.<br>
   <br>

- `ILayoutController` 를 구현하는 컴포넌트<br>
  - `LayoutGroup` (`VerticalLayoutGroup`, `HorizontalLayoutGroup`, `GridLayoutGroup` 등)<br>
  <br>: `LayoutGroup` 컴포넌트들은 `ILayoutController` 인터페이스를 구현하여, 자식 요소들의 위치와 크기를 <b>직접적으로</b> 조정한다.<br>
  <br>
  - `ContentSizeFitter` (`ILayoutElement` 또한 구현)<br>
  <br>: `ILayoutController` 인터페이스를 구현하여, 자식 요소의 크기 변경에 따라 부모 요소의 크기를 동적으로 조정한다.<br>

<br>
<br>
<br>
<br>

## Pre-Rebuild Layout Phase
이 단계는 레이아웃 갱신 과정에서 '초기 준비와 설정' 을 담당하는 단계라고 할 수 있다.<br>
<br>
즉, `UI` 요소들의 레이아웃이 실제로 계산되고 적용되기 전에, 레이아웃 시스템이 필요한 사전 정보를 수집하고 준비하는 과정이다.<br>
<br>
이를 통해 후속 단계에서의 레이아웃 계산과 적용이 원활하게 이루어질 수 있도록 한다.<br>
<br>
이러한 '레이아웃 계산을 위한 중요한 기반' 을 `Pre-Rebuild Layout Phase` 에서 마련한다.<br>
<br>
`UI` 요소들의 레이아웃이 효율적이고 정확하게 계산되기 위해서는, <b>각 요소의 레이아웃 관련 속성과 제약 조건이 사전에 명확하게 정의되어 있어야</b> 하는데,<br>
<br>
`Pre-Rebuild Layout Phase` 는 이러한 사전 준비 작업을 수행하여, 레이아웃 시스템이 최적의 조건에서 작동할 수 있도록 돕는 것이다.<br>
<br>
<br>
<br>

### 연관 인터페이스 : ILayoutController
`ILayoutController` 인터페이스는 이 단계에서 핵심적인 역할을 수행한다.<br>
<br>
이 인터페이스를 구현하는 컴포넌트(예 : LayoutGroup, ContentSizeFitter 등)는 레이아웃의 조정과 적용을 <b>직접적으로</b> 담당하며,<br>
<br>
`Pre-Rebuild Layout Phase` 에서 필요한 사전 계산과 설정 작업을 수행한다.<br>
<br>
<br>
<br>

### 작동 방식
`ILayoutController` 인터페이스를 구현하는 컴포넌트들은 다음과 같은 작업을 `Pre-Rebuild Layout Phase` 에서 수행한다.<br>
<br>

<b>자식 요소들의 크기와 배치 조건 확인</b><br>
<br>: `LayoutGroup` 컴포넌트와 같은 레이아웃 컨트롤러는 자식 요소들의 레이아웃 관련 속성(예 : 최소 크기, 선호 크기, 유연 크기 등)을 검토하고,<br>
<br>
이를 바탕으로 자식 요소들이 어떻게 배치될지에 대한 초기 조건을 설정한다.<br>
<br>

<b>사전 계산 수행</b><br>
<br>: 레이아웃 계산에 필요한 사전 정보(예 : 총 사용 가능한 공간, 자식 요소들 간의 간격 등)를 계산한다.<br>
<br>
이는 실제 레이아웃 계산이 수행되기 전에 필요한 <b>'준비 작업'</b> 으로, 레이아웃 계산의 효율성과 정확성을 높이기 위함이다.<br>
<br>

<b>레이아웃 관련 속성 설정</b><br>
<br>: 각 `UI` 요소의 `RectTransform` 에 적용될 레이아웃 관련 속성(예 : 앵커, 피봇, 오프셋 등)을 사전에 설정한다.<br>
<br>
즉, `UI` 요소들이 어떻게 배치되고 크기가 조정될지에 대한 기본적인 조건을 제공하는 것이다.<br>
<br>
<br>
<br>
<br>

## Calculation Phase
이 단계는 `Layout Update Cycle` 의 핵심적인 단계 중 하나로, `UI` 요소의 크기와 구조를 결정하는 데 <b>필수적인 레이아웃 계산이 수행되는 단계</b>이다.<br>
<br>
이 단계에서는 `ILayoutElement` 인터페이스를 구현하는 모든 컴포넌트의 레이아웃 속성들이 평가되고, 각 요소의 최종 크기와 배치가 계산된다.<br>
<br>
<br>
<br>

### 연관 인터페이스 : ILayoutElement
`ILayoutElement` 인터페이스를 구현하는 컴포넌트들이 `Calculation Phase` 에서 수행되는 레이아웃 계산에 중요한 역할을 한다.<br>
<br>
이 인터페이스는 다음과 같은 메서드들을 포함한다.<br>
<br>
<br>
<b>CalculateLayoutInputHorizontal()</b><br>
<br>: `UI` 요소의 수평 방향에 대한 레이아웃 입력을 계산한다.<br>
<br>
<b>CalculateLayoutInputVertical()</b><br>
<br>: `UI` 요소의 수직 방향에 대한 레이아웃 입력을 계산한다.<br>
<br>
<br>

위 두 메서드들을 통하여 각 `UI` 요소의 최소 크기, 선호 크기, 그리고 유연성을 결정하게 된다.<br>
<br>
<br>
<br>

### 작동 방식
해당 단계의 작동 방식에 대한 특징은 다음과 같다.<br>
<br>

<b>Bottom-Up 계산</b><br>
<br>: 레이아웃 계산은 하위 요소에서부터 시작하여 상위 요소로 진행되는 `bottom-up` 방식으로 수행된다.<br>
<br>
이러한 접근 방식은 '자식 요소들의 크기와 요구 사항을 먼저 고려'하여 '부모 요소의 크기와 배치를 결정' 할 수 있도록 하기 위함이다.<br>
<br>

<b>자식 요소의 크기 고려</b><br>
<br>: 각 `UI` 요소는 자신의 `ILayoutElement` 구현을 통해 자식 요소들의 크기 요구 사항을 고려하여 자신의 크기를 결정한다.<br>
<br>
예를 들어, `ContentSizeFitter` 컴포넌트를 사용하는 `UI` 요소는 '자식 요소들의 총 크기' 에 기반하여 '자신의 크기' 를 조정한다.<br>
<br>

<b>ContentSizeFitter 의 역할</b><br>
<br>: `ContentSizeFitter` 는 `ILayoutElement` 를 구현하는 컴포넌트 중 하나로, 자식 요소의 크기에 따라 `UI` 요소의 크기를 동적으로 조정한다.<br>
<br>
이 컴포넌트는 자식 요소들의 `CalculateLayoutInputHorizontal` 및 `CalculateLayoutInputVertical` 메서드의 결과를 사용하여, 부모 요소의 최소 및 선호 크기를 결정하게 된다.<br>
<br>
<br>
<br>
<br>

## Set Layout Phase
이 단계는 `Unity GUI` 시스템에서 레이아웃 계산 과정을 통해 결정된 레이아웃 정보를 <b>실제 `UI` 요소에 적용하는 단계</b>이다.<br>
<br>
즉, 이 단계를 통해 `UI` 요소들의 최종적인 크기와 위치를 확정짓고, 화면에 정확하게 배치하게 된다.<br>
<br>
<br>
<br>

### 연관 인터페이스 : ILayoutController
이 단계에서는 `ILayoutController` 인터페이스를 구현하는 컴포넌트들이 핵심적인 역할을 한다.<br>
<br>
이 인터페이스는 다음과 같은 메서드들을 포함한다.<br>
<br>
<br>
<b>SetLayoutHorizontal()</b><br>
<br>: 수평 방향의 레이아웃을 설정한다.<br>
<br>

<b>SetLayoutVertical()</b><br>
<br>: 수직 방향의 레이아웃을 설정한다.<br>
<br>

즉, 위 메서드들을 통하여 이전 단계들로부터의 레이아웃 정보를 실제 `UI` 요소들에게 적용하게 된다.<br>
<br>
<br>
<br>

### 작동 방식
해당 단계의 작동 방식에 대한 특징은 다음과 같다.<br>
<br>

<b>Top-Down 레이아웃 적용</b><br>
<br>: 레이아웃 적용 과정은 상위 요소에서 시작하여 하위 요소로 진행되는 `top-down` 방식으로 수행된다.<br>
<br>
이를 통해 '부모 요소의 레이아웃 설정' 이 '자식 요소들의 배치' 에 영향을 미칠 수 있도록 한다.<br>
<br>

<b>LayoutGroup 의 역할</b><br>
<br>: `LayoutGroup` 컴포넌트들은 `ILayoutController` 인터페이스를 구현하므로,<br>
<br>
`SetLayoutHorizontal` 및 `SetLayoutVertical` 메서드를 사용하여, 자식 요소들을 계산된 레이아웃 정보에 따라 적절히 배치하고 크기를 조정한다.<br>
<br>

<b>RectTransform 의 조정</b><br>
<br>: 실제 레이아웃 적용은 각 `UI` 요소의 `RectTransform` 에 대한 크기와 위치 속성의 조정을 통해 이루어진다.<br>
<br>
즉, `LayoutGroup` 컴포넌트들은 자식 요소들의 `RectTransform` 속성을 갱신하여, 계산된 레이아웃 정보를 반영하게 된다.<br>
<br>
<br>
<br>
<br>

## Finalization Phase
이 단계는 `Unity GUI` 시스템에서 레이아웃 적용 과정이 완료된 후에 수행되는 최종 조정 단계이다.<br>
<br>
이 단계의 목적은 `UI` 요소들이 사용자에게 표시되기 직전, 레이아웃의 세부 사항을 미세 조정하여 시각적 균형, 정렬 등을 개선하는 것이다.<br>
<br>
즉, 보다 더 정교하고 일관된 사용자 경험을 위하여 `UI` 품질을 향상시키는 단계이다.<br>
<br>
<br>
<br>

### 연관 컴포넌트
`Finalization Phase` 와 연관된 컴포넌트는 다음과 같다.<br>
<br>

<b>LayoutGroup</b><br>
<br>: 이 단계에서 `LayoutGroup` 컴포넌트들은 자식 요소들 사이의 간격과 정렬을 최종적으로 조정한다.<br>
<br>
또한, 여백(Margin)과 패딩(Padding)을 적용하며, 요소간의 시각적 간격을 최적화한다.<br>
<br>

<b>ContentSizeFitter</b><br>
<br>: 이 단계에서 `ContentSizeFitter` 컴포넌트는 자식 요소들의 최종 크기를 기반으로 부모 요소의 크기를 최종적으로 조정함으로 `UI` 가 콘텐츠에 따라서 동적으로 반응할 수 있도록 한다.<br>
<br>
<br>
<br>

### 작동 방식
해당 단계의 작동 방식에 대한 특징은 다음과 같다.<br>
<br>

<b>세부 조정</b><br>
<br>: 각 `LayoutGroup` 컴포넌트는 자신의 레이아웃 규칙에 따라 자식요소들의 배치를 최종적으로 조정한다.<br>
<br>
이는 요소들 사이의 간격, 정렬 방식, 그리고 필요한 경우 추가 여백이나 패딩의 적용을 포함한다.<br>
<br>

<b>동적 크기 조정</b><br>
<br>: `ContentSizeFitter` 를 사용하는 `UI` 요소들은 이 단계에서 콘텐츠의 최종 크기에 따라 동적으로 크기가 조정된다.<br>
<br>
이를 통해 `UI` 는 콘텐츠의 양이 변화해도 일관된 레이아웃을 유지할 수 있게 된다.<br>
<br>

<b>최종 확정</b><br>
<br>: 모든 조정 작업이 완료되면, 각 `UI` 요소의 `RectTransform` 은 최종적인 크기와 위치 값으로 설정된다.<br>
<br>
이 단계의 결과는 `UI` 요소들이 화면에 그려지기 직전의 최종 레이아웃 상태를 반영한다.<br>
<br>
<br>
<br>
<br>

## Rendering Phase
이 단계는 `UI` 요소들이 사용자의 화면에 실제로 그려지는 단계이다.<br>
<br>
이 과정은 `Unity` 의 `렌더링 파이프라인` 에 의해 처리된다.<br>
<br>
<br>
<br>

### 연관 컴포넌트
`UI` 시스템의 `Rendering Phase` 와 연관된 컴포넌트는 다음과 같다.<br>
<br>

<b>Canvas</b><br>
<br>: `Canvas` 컴포넌트는 `UI` 요소들의 렌더링 순서와 방식을 관리하며, 모든 자식 `UI` 요소들이 이 `Canvas` 내에서 렌더링된다.<br>
<br>

<b>Graphic 컴포넌트</b><br>
<br>: 각 `Graphic` 컴포넌트는 자체적인 렌더링 데이터(색상, 텍스쳐, 텍스트 등)를 가지며, 이 데이터가 렌더링 과정에서 화면에 그려진다.<br>
<br>

<b>CanvasRenderer</b><br>
<br>: `Graphic` 컴포넌트로부터 렌더링 데이터를 받아 실제로 화면에 그리는 역할을 하는 컴포넌트이다.<br>
<br>
이 컴포넌트를 통해 렌더링 데이터를 최적화하고, 필요한 그래픽 명령을 생성하여 `GPU` 에게 전달하게 된다.<br>
<br>
<br>
<br>

### 작동 방식
해당 단계의 작동 방식에 대한 특징은 다음과 같다.<br>
<br>

<b>렌더링 순서 결정</b><br>
<br>: `Canvas` 컴포넌트는 자식 `UI` 요소들의 렌더링 순서를 결정한다.<br>
<br>
다만, 이는 `UI` 요소들의 계층 구조와 `Canvas` 의 렌더링 설정 등에 따라서 달라질 수 있다.<br>
<br>

<b>Graphic 컴포넌트 처리</b><br>
<br>: 각 `Graphic` 컴포넌트는 자신의 시각적 데이터를 준비하고, 이를 `CanvasRenderer` 에게 전달한다.<br>
<br>
예를 들어, `Text` 컴포넌트는 텍스트를 렌더링하기 위한 데이터를, `Image` 컴포넌트는 이미지를 렌더링하기 위한 텍스쳐와 `UV` 매핑 정보를 제공한다.<br>
<br>

<b>CanvasRenderer에 의한 렌더링</b><br>
<br>: `CanvasRenderer` 는 받은 렌더링 데이터를 기반으로 그래픽 명령을 실행하고, 이를 `Unity` 렌더링 파이프라인에 전달한다.<br>
<br>
이 과정에서, `UI` 요소들은 최적화된 방식으로 화면에 렌더링 된다.<br>
<br>

<b>화면에 표시</b><br>
<br>: 최종적으로, `UI` 요소들의 시각적 표현이 사용자의 화면에 그려진다.<br>
<br>
이것이, 드디어 사용자가 볼 수 있는 `UI` 의 결과물이 된다.<br>
<br>
<br>
<br>
참고 : [[Manual]Unity UI: Unity User Interface](https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/index.html)
<br>
<br>
<br>
