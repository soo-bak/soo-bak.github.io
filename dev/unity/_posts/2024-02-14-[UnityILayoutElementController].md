---
layout: single
title: "Unity GUI 의 ILayoutElement, ILayoutController - soo:bak"
date: "2024-02-14 00:51:00 +0900"
---
<br>

`Unity` 에서 `ILayoutElement` 와 `ILayoutElement` 인터페이스는 `Unity` 의 `UI` 시스템인 `UGUI` 에서 레이아웃을 관리하는 데 사용된다.<br>
<br>
이 인터페이스들은 `Unity` 엔진 내부의 `C#` 인터페이스로 정의되어있으며, `Unity` 의 소스 코드가 공개적으로 제공되지 않기 때문에,<br>
<br>
정확한 코드 구현을 알 수는 없지만,<br>
<br>
공식 사이트에 공개된 매뉴얼을 바탕으로 기본적인 목적과 메서드의 선언과 원형에 대해서는 파악할 수 있다.<br>
<br>
<br>
<br>

## ILayoutElement
`ILayoutElement` 인터페이스는 `UI` 요소가 <u>레이아웃 시스템에 참여하기 위해</u> 구현해야하는 인터페이스이다.<br>
<br>
이 인터페이스를 통해 `UI` 요소는 <b>자신의 레이아웃 관련 속성(예 : 최소 크기, 선호 크기, 유연성 등)을 레이아웃 시스템에 제공</b>하게 된다.<br>
<br>
<br>
<br>
<b>[ILayoutElement]</b><br>

```c#
public interface ILayoutElement {
  void CalculateLayoutInputHorizontal();
  void CalculateLayoutInputVertical();

  float minWidth { get; }
  float preferredWidth { get; }
  float flexibleWidth { get; }
  float minHeight { get; }
  float preferredHeight { get; }
  float flexibleHeight { get; }
  int layoutPriority { get; }
}
```
<br>

`CalculateLayoutInputHorizontal()` , `CalculateLayoutInputVertical` <b>메서드</b><br>
<br>: `UI` 요소가 <b>자신</b>의 수평/수직 방향의 레이아웃 입력을 계산할 때 호출됨<br>
<br>

`minWidth`, `preferredWidth`, `flexibleWidth`, `minHeight`, `preferredHeight`, `flexibleHeight` <b>속성</b><br>
<br>: 각각 `UI` 요소의 최소 크기, 선호 크기, 유연성을 나타냄<br>
<br>

`layoutPriority` <b>속성</b><br>
<br>: 레이아웃 시스템이 여러 요소들 사이의 레이아웃을 계산할 때 요소의 우선순위를 결정함<br>
<br>
<br>
<br>

### ILayoutElement 를 구현하는 컴포넌트들
<br>

`LayoutElement`<br>
<br>: 개발자가 수동으로 `UI` 요소의 최소, 선호, 유연 크기를 설정할 수 있게 해주며,<br>
<br>
이를 통해 해당 `UI` 요소의 레이아웃을 더 세밀하게 제어할 수 있도록 한다.<br>
<br>
<br>

`ContentSizeFitter`<br>
<br>: 자식 요소들의 크기에 따라 부모 요소의 크기를 조정한다.<br>
<br>
이 컴포넌트는 `ILayoutElement` 인터페이스를 통해 자식 요소들의 크기 요구사항을 레이아웃 시스템에 전달한다.<br>
<br>
<br>

`Text`, `Image`, `RawImage`<br>
<br>: 텍스트, 이미지의 내용과 크기, 스타일 등에 따라 자신의 선호 크기를 계산한다.<br>
<br>
<br>
<br>
<br>

## ILayoutController
`ILayoutController` 인터페이스는 `UI` 요소가 레이아웃을 <b>직접</b> 조정할 수 있도록 하는 메서드를 정의한다.<br>
<br>
`LayoutGroup` 과 같은 컴포넌트가 이 인터페이스를 구현하여 자식 요소들의 레이아웃을 관리한다.<br>
<br>
<br>
<br>
<b>[ILayoutController]</b><br>

```c#
public interface ILayoutController {
  void SetLayoutHorizontal();
  void SetLayoutVertical();
}
```
<br>

`SetLayoutHorizontal()` , `SetLayoutVertical()` <b>메서드</b><br>
<br>: 레이아웃 시스템이 `UI` 요소의 수평 및 수직 레이아웃을 조정할 때 사용<br>
<br>
<br>
<br>

### ILayoutController 를 구현하는 컴포넌트들
<br>

`LayoutGroup`<br>
<br>: 여러 자식 `UI` 요소들을 관리하는 <b>추상 기본 클래스</b>로, `VerticalLayoutGroup`, `HorizontalLayoutGroup`, `GridLayoutGroup` 등이 `LayoutGroup` 을 상속 받아 특정 레이아웃 패턴을 구현한다.<br>
<br>
<br>

`VerticalLayoutGroup`<br>
<br>: 자식 요소들을 수직으로 정렬한다.<br>
<br>

`HorizontalLayoutGroup`<br>
<br>: 자식 요소들을 수평으로 정렬한다.<br>
<br>

`GridLayoutGroup`<br>
<br>: 자식 요소들을 그리드 형태로 정렬한다.<br>
<br>
셀의 크기, 간격, 그리고 정렬 방식을 설정할 수 있으며, 그리드 레이아웃을 조정한다.<br>
<br>
<br>
<br>

참고 : [[Manual]Unity UI: Unity User Interface](https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/index.html)
<br>
<br>
<br>
