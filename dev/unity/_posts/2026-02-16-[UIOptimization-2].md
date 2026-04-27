---
layout: single
title: "UI 최적화 (2) - UI 최적화 전략 - soo:bak"
date: "2026-02-16 22:50:00 +0900"
description: Canvas 분리, ScrollRect 풀링, TextMeshPro, 폰트 아틀라스, UI 오버드로우, Raycast Target을 설명합니다.
tags:
  - Unity
  - 최적화
  - UI
  - UGUI
  - 모바일
---

## 하나의 Canvas가 만드는 문제

[Part 1](/dev/unity/UIOptimization-1/)에서 확인했듯 Canvas 리빌드는 Canvas 단위로 발생하므로, 요소 하나만 바뀌어도 그 Canvas 전체의 메쉬가 다시 계산됩니다.

그래서 모든 UI를 하나의 Canvas에 담으면 값 하나가 바뀔 때마다 화면 전체 UI를 다시 그리는 셈이 됩니다. 그런데 실제 게임 UI는 성격이 다른 요소들이 섞여 있습니다.

체력바·스코어처럼 매 프레임 갱신되는 요소가 있는가 하면, HUD 테두리·배경 프레임처럼 전투 내내 고정된 요소도 함께 있습니다.

이들을 같은 Canvas에 두면 스코어 숫자 하나가 바뀔 때마다 바뀌지 않은 테두리와 배경까지 매번 재배칭되고, 요소가 많을수록 이 낭비가 프레임마다 쌓여 프레임 드랍으로 이어집니다.

이어지는 섹션에서는 Canvas를 어떻게 쪼개야 하는지부터 시작해, 리스트·텍스트·오버드로우처럼 Canvas 밖에서 발생하는 비용까지 단계별로 살펴봅니다.

---

## Canvas 분리 — 정적 요소와 동적 요소

Canvas를 분리하려면 먼저 어떤 기준으로 UI 요소를 구분할지 정해야 합니다.

가장 직관적인 기준은 변경 빈도이고, 이에 따라 요소를 정적과 동적으로 나눠 각각 다른 Canvas에 배치합니다.

### 정적 Canvas와 동적 Canvas

정적 요소는 배경 이미지·장식 프레임·고정 아이콘·타이틀 텍스트처럼 한 번 그려지면 게임이 끝날 때까지 모양이 변하지 않는 UI이고,

동적 요소는 점수·타이머·HP 바·쿨다운 표시·콤보 카운터처럼 매 프레임이나 빈번한 이벤트마다 값이 갱신되는 UI입니다.

전자는 초기에 한 번만 메쉬가 만들어지면 그 뒤로는 다시 계산될 일이 없고, 후자는 값이 바뀔 때마다 리빌드가 새로 실행됩니다.

<br>

이 둘을 같은 Canvas에 함께 배치하면 동적 요소가 바뀔 때마다 정적 요소의 메쉬까지 함께 재계산됩니다.

서로 다른 Canvas로 분리하면 동적 Canvas만 재계산되고, 정적 Canvas는 최초에 그려둔 메쉬를 이후 프레임에서 그대로 재사용하므로, 해당 요소가 변하지 않는 동안은 추가 리빌드 비용이 발생하지 않습니다.

<br>

### 구현 — 루트 Canvas와 Sub-Canvas

Canvas 분리는 **새로운 Canvas 컴포넌트를 추가**하는 것으로 구현됩니다.

컴포넌트를 씬의 독립 오브젝트에 붙이면 별도의 **루트 Canvas**가 생기고, 기존 Canvas의 자식 오브젝트에 붙이면 **Sub-Canvas(Nested Canvas)** 가 만들어집니다.

두 방식 모두 Canvas가 독립된 배칭·리빌드 단위라는 점은 같으며, 차이는 렌더 설정의 독립성에 있습니다.

루트 Canvas는 렌더 모드·카메라·해상도 참조 같은 속성을 각자 갖고, Sub-Canvas는 부모 Canvas의 렌더 설정을 상속하면서 배칭과 리빌드만 별개 단위로 동작합니다.

하나의 UI 계층 안에서 정적·동적 요소만 나누려는 경우에는 Sub-Canvas가 자연스러운 선택입니다.
공통 렌더 설정은 부모 Canvas가 관리하고, 자식 Canvas는 리빌드 경계 역할만 맡기 때문입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- Root Canvas -->
  <rect x="170" y="15" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="38" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Root Canvas</text>
  <text x="370" y="38" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 최상위 Canvas</text>

  <!-- Vertical line from Root -->
  <line x1="260" y1="51" x2="260" y2="80" stroke="currentColor" stroke-width="1.5"/>

  <!-- Horizontal branch line -->
  <line x1="130" y1="80" x2="390" y2="80" stroke="currentColor" stroke-width="1.5"/>

  <!-- Left vertical to Static -->
  <line x1="130" y1="80" x2="130" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <!-- Right vertical to Dynamic -->
  <line x1="390" y1="80" x2="390" y2="100" stroke="currentColor" stroke-width="1.5"/>

  <!-- Left arrow -->
  <polygon points="130,100 126,93 134,93" fill="currentColor"/>
  <!-- Right arrow -->
  <polygon points="390,100 386,93 394,93" fill="currentColor"/>

  <!-- Static Sub-Canvas box -->
  <rect x="25" y="102" width="210" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="125" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Static Sub-Canvas</text>

  <!-- Static label -->
  <text x="130" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Canvas 컴포넌트 추가 · 정적</text>

  <!-- Dynamic Sub-Canvas box -->
  <rect x="285" y="102" width="210" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="125" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Dynamic Sub-Canvas</text>

  <!-- Dynamic label -->
  <text x="390" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Canvas 컴포넌트 추가 · 동적</text>

  <!-- Vertical lines from Sub-Canvas boxes to children -->
  <!-- Static side -->
  <line x1="130" y1="160" x2="130" y2="185" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <!-- Dynamic side -->
  <line x1="390" y1="160" x2="390" y2="185" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>

  <!-- Static children -->
  <rect x="40" y="185" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="206" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Background Image</text>

  <rect x="40" y="227" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Frame Image</text>

  <rect x="40" y="269" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="290" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Fixed Icon</text>

  <!-- Connector lines between static children -->
  <line x1="130" y1="219" x2="130" y2="227" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="130" y1="261" x2="130" y2="269" stroke="currentColor" stroke-width="1" opacity="0.4"/>

  <!-- Dynamic children -->
  <rect x="300" y="185" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="206" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Score Text</text>

  <rect x="300" y="227" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Timer Text</text>

  <rect x="300" y="269" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="290" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">HP Bar</text>

  <!-- Connector lines between dynamic children -->
  <line x1="390" y1="219" x2="390" y2="227" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="390" y1="261" x2="390" y2="269" stroke="currentColor" stroke-width="1" opacity="0.4"/>

  <!-- Grouping brackets / labels at bottom -->
  <line x1="40" y1="315" x2="220" y2="315" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <text x="130" y="335" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">리빌드 발생 안 함</text>
  <text x="130" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(변경 없는 요소)</text>

  <line x1="300" y1="315" x2="480" y2="315" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <text x="390" y="335" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">이 Canvas만 리빌드</text>
  <text x="390" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(자주 변하는 요소)</text>

</svg>
</div>

위 구조에서 Dynamic Sub-Canvas에 속한 Score Text나 HP Bar의 값이 바뀌면, 재계산은 해당 Canvas 안에서만 일어납니다.

Static Sub-Canvas에 담긴 Background Image와 Frame Image는 메쉬가 그대로 유지되며, 부모 Root Canvas도 직접 영향을 받지 않습니다.

각 Canvas가 자신에 속한 요소만 독립적으로 배칭하므로, 리빌드는 Canvas 경계를 넘어 전파되지 않습니다.

대신 Canvas 수가 늘수록 드로우콜도 증가합니다. Canvas는 각각 독립된 배칭 경계이므로, 같은 머티리얼·텍스처를 쓰는 요소라도 Canvas가 다르면 한 번에 합쳐지지 못하고 별도의 드로우콜로 제출됩니다.

<br>

그럼에도 분리가 유리한 이유는 리빌드 비용이 훨씬 무겁기 때문입니다.

리빌드는 Canvas에 속한 모든 요소의 메쉬를 다시 수집하고 배칭하는 CPU 작업이라 요소 수에 비례해 커지는 반면, 드로우콜 한두 개 추가는 Canvas당 거의 고정된 오버헤드에 가깝습니다.

예를 들어 100개 요소가 한 Canvas에 모여 있을 때 매 프레임 전체를 재계산하는 비용은, 정적 99개와 동적 1개를 별도 Canvas로 분리해 동적 Canvas만 재계산하고 드로우콜 하나를 더 감수하는 비용보다 훨씬 큽니다.

<br>

### 분리 기준

Canvas를 몇 개로 분리할지는 프로젝트마다 다르지만, 기본 기준은 변경 빈도입니다.

매 프레임 변하는 요소와 전혀 변하지 않는 요소가 같은 Canvas에 있으면, 정적 요소까지 매 프레임 재배칭되므로 분리 효과가 가장 큽니다.

---

## ScrollRect 풀링 — 긴 리스트의 최적화

Canvas 분리는 리빌드 범위를 여러 Canvas로 나누는 방식이지만, 리스트처럼 아이템이 수백~수천 개에 이르는 UI에서는 Canvas를 분리해도 각 Canvas의 요소 수가 여전히 많습니다.

ScrollRect 풀링은 Canvas 안에 실제로 생성하는 UI 오브젝트 수를 줄이는 방법입니다.

### ScrollRect의 문제

채팅 로그·인벤토리·상점 목록·랭킹 같은 긴 리스트는 게임 UI에서 자주 등장하며, 대부분 Unity의 **ScrollRect** 컴포넌트로 구현됩니다.

ScrollRect는 지정한 뷰포트 안에 스크롤 가능한 영역을 만들어 주고, 개발자는 그 영역 안에 아이템들을 세로나 가로로 배치해 리스트를 완성합니다.

그런데 별다른 최적화 없이 구현하면 리스트의 아이템 수만큼 UI GameObject를 처음부터 생성하게 됩니다.

아이템이 1,000개인 인벤토리라면 UI GameObject도 1,000개가 만들어지고, 각 아이템이 아이콘·이름·수량·등급 같은 자식 요소를 포함하므로 실제 오브젝트 수는 수천 개에 이릅니다.

이 수천 개가 모두 같은 Canvas에 속해 있다면, 값 하나만 바뀌어도 Canvas는 수천 개 전체의 메쉬를 다시 수집하고 배칭하게 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기본 ScrollRect 구현의 문제</text>

  <!-- ========== 왼쪽: 화면에 보이는 영역 (뷰포트) ========== -->
  <text x="155" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">화면에 보이는 영역 (10개)</text>

  <!-- 뷰포트 외곽 박스 -->
  <rect x="30" y="60" width="250" height="222" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 아이템 1 -->
  <rect x="45" y="70" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <rect x="52" y="74" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5"/>
  <text x="75" y="86" font-family="sans-serif" font-size="10" fill="currentColor">아이템 1</text>
  <rect x="130" y="74" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <text x="150" y="86" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">아이콘</text>
  <rect x="185" y="74" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <text x="205" y="86" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">이름</text>

  <!-- 아이템 2 -->
  <rect x="45" y="98" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <rect x="52" y="102" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5"/>
  <text x="75" y="114" font-family="sans-serif" font-size="10" fill="currentColor">아이템 2</text>
  <rect x="130" y="102" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="185" y="102" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>

  <!-- 아이템 3 -->
  <rect x="45" y="126" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <rect x="52" y="130" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5"/>
  <text x="75" y="142" font-family="sans-serif" font-size="10" fill="currentColor">아이템 3</text>
  <rect x="130" y="130" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="185" y="130" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>

  <!-- 생략 표시 -->
  <text x="155" y="170" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">···</text>

  <!-- 아이템 9 -->
  <rect x="45" y="182" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <rect x="52" y="186" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5"/>
  <text x="75" y="198" font-family="sans-serif" font-size="10" fill="currentColor">아이템 9</text>
  <rect x="130" y="186" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="185" y="186" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>

  <!-- 아이템 10 -->
  <rect x="45" y="210" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8"/>
  <rect x="52" y="214" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5"/>
  <text x="75" y="226" font-family="sans-serif" font-size="10" fill="currentColor">아이템 10</text>
  <rect x="130" y="214" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="185" y="214" width="16" height="16" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>

  <!-- ========== 오른쪽: 화면 밖 영역 ========== -->
  <text x="405" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">화면 밖 (990개)</text>

  <!-- 화면 밖 영역 박스 — 점선 테두리 -->
  <rect x="300" y="60" width="210" height="222" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 3" opacity="0.5"/>

  <!-- 화면 밖 아이템들 — 반투명 -->
  <rect x="315" y="70" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="84" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 11</text>
  <text x="460" y="84" text-anchor="end" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.3">← 화면 밖</text>

  <rect x="315" y="94" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="108" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 12</text>
  <text x="460" y="108" text-anchor="end" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.3">← 화면 밖</text>

  <rect x="315" y="118" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="132" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 13</text>

  <rect x="315" y="142" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="156" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 14</text>

  <!-- 생략 표시 -->
  <text x="405" y="182" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.3">···</text>

  <rect x="315" y="194" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="208" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 999</text>

  <rect x="315" y="218" width="180" height="20" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.6" opacity="0.35"/>
  <text x="325" y="232" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">아이템 1000</text>
  <text x="460" y="232" text-anchor="end" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.3">← 화면 밖</text>

  <!-- ========== 하단: 비교 바 ========== -->
  <!-- Canvas 리빌드 대상 전체 바 -->
  <text x="260" y="310" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Canvas 리빌드 대상</text>
  <rect x="30" y="318" width="480" height="22" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="333" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1,000개 전체</text>

  <!-- 실제 화면에 보이는 비율 바 -->
  <text x="260" y="358" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">실제 화면에 보이는 아이템</text>
  <rect x="30" y="366" width="48" height="22" rx="4" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="54" y="381" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">10개</text>

  <!-- 비율 점선 -->
  <line x1="84" y1="377" x2="506" y2="377" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3 2" opacity="0.2"/>

  <!-- 결론 텍스트 -->
  <text x="260" y="412" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">1,000개 전체가 Canvas 리빌드 대상이지만, 화면에 보이는 것은 10개</text>

</svg>
</div>

다이어그램에서 드러나듯, 사용자가 실제로 보는 것은 10개 남짓이지만 Canvas는 화면 밖에 있는 990개까지 포함해 1,000개 전체를 리빌드 대상으로 삼습니다.

뷰포트 바깥에 있어 화면에 그려지지도 않는 요소들이 같은 Canvas의 자식이라는 이유만으로 메모리를 점유하고 리빌드 비용에 합산되며, 리스트를 처음 여는 순간 1,000개 전체를 생성하는 시간이 그대로 초기 로딩 지연으로 쌓입니다.

### 풀링의 원리

ScrollRect 풀링은 실제로 화면에 보이는 아이템과 스크롤 여분만 GameObject로 생성합니다.

화면에 10개가 동시에 보이는 리스트라면 스크롤 경계를 잠시 드나드는 여분까지 합쳐 13~15개만 GameObject로 만들고, 나머지 985~987개는 데이터(이름·수량·아이콘 경로 등)로만 메모리에 남겨 둡니다.

이 상태에서 사용자가 리스트를 스크롤하면 화면 위쪽으로 사라진 오브젝트가 그대로 아래쪽 위치로 옮겨지고, 이 오브젝트의 내용은 새로 들어올 아이템의 데이터로 교체됩니다.

GameObject의 생성·파괴는 일어나지 않고 같은 15개의 오브젝트가 계속 재활용되며 서로 다른 데이터를 표시할 뿐입니다.

일반적인 오브젝트 풀링이 '사용 중'과 '대기 중' 상태 관리에 그치는 반면, ScrollRect 풀링은 위치 이동과 데이터 교체까지 매 프레임 수행한다는 점에서 다릅니다.

### 풀링의 효과

풀링을 적용하면 리빌드·메모리·초기 생성의 세 가지 비용이 한꺼번에 줄어듭니다.

Canvas 리빌드에서 처리할 UI 요소가 1,000개에서 15개 수준으로 떨어져 1회 리빌드의 CPU 비용이 크게 가벼워지고, 메모리에 상주하는 GameObject·컴포넌트·메쉬 데이터도 같은 비율로 감소하며, 각 아이템이 아이콘·이름·수량·등급 같은 자식 요소를 여러 개 포함할수록 절약 폭은 더 커집니다.

초기 로딩의 부담도 줄어듭니다.

풀링 방식에서는 1,000개 대신 15개만 만들면 되므로 리스트를 처음 여는 순간 발생하던 프레임 끊김이 사라지고, 목록이 거의 즉시 화면에 표시됩니다.

이후 스크롤 중에도 새 오브젝트를 만들지 않고 기존 오브젝트의 데이터만 교체하기 때문에 생성 비용이 다시 발생하지 않습니다.

---

## TextMeshPro vs Legacy Text

UI에서 텍스트는 값이 자주 바뀌는 대표적인 요소입니다. 점수·시간·체력 수치처럼 매 프레임 갱신되는 텍스트가 많고, 그때마다 메쉬가 다시 만들어집니다.

어떤 텍스트 컴포넌트를 선택하느냐에 따라 이 갱신 비용과 렌더링 품질이 달라집니다.

### Legacy Text의 한계

Legacy Text는 비트맵 기반 텍스트 렌더링을 사용합니다.

폰트의 각 글자를 특정 크기로 래스터화(비트맵 이미지로 변환)해 텍스처에 저장해 두고, 텍스트를 그릴 때 그 텍스처에서 글자를 읽어와 메쉬를 구성하는 방식입니다.

이 방식에서는 텍스트 내용이 바뀌면 메쉬가 통째로 다시 만들어지며, 글자의 정점 위치와 UV가 모두 새로 계산되고 글자 수가 달라지면 정점 수와 버퍼 크기까지 함께 변합니다.

저장된 비트맵은 특정 크기에 맞춰져 있어 글자를 확대하거나 축소하면 흐려지거나 깨지므로, 다양한 크기를 지원하려면 같은 폰트를 여러 크기로 래스터화해 둬야 하고 폰트 텍스처도 그만큼 커집니다.

여기에 기존 텍스처에 없는 글자가 등장하면 런타임에 래스터화해 추가하면서 텍스처 업로드가 발생하고, 같은 폰트를 쓰는 다른 텍스트까지 그 갱신의 영향을 받습니다.

이 비용들은 모두 글자를 비트맵으로 저장해 두고 읽어오는 구조에서 비롯되므로, 갱신 비용을 줄이려면 비트맵을 전제하지 않는 다른 렌더링 방식이 필요합니다.

### TextMeshPro의 SDF 렌더링

**TextMeshPro(TMP)** 는 **SDF(Signed Distance Field)** 기반의 텍스트 렌더링을 사용하며, 비트맵 방식과의 차이는 텍스처에 저장하는 데이터에 있습니다.

비트맵 방식에서 각 텍셀(텍스처 픽셀)은 글자의 불투명도를 저장하고, 텍스처는 특정 크기에 맞춰 미리 래스터화되어 있습니다.

글자를 그보다 크게 표시하면 같은 픽셀 데이터가 더 넓은 영역에 늘어나면서 가장자리에 계단 현상이 생기므로, 다양한 크기를 깨끗하게 지원하려면 크기별로 별도의 비트맵을 미리 만들어 두어야 합니다.

반면 SDF 텍스처의 각 텍셀은 색상이 아니라 **글자 윤곽선까지의 거리**를 저장합니다.

내부 텍셀은 양수, 외부는 음수, 윤곽선 위는 0이며, 렌더링 시점에 GPU의 프래그먼트 셰이더가 이 거리 값을 읽어 임계값을 기준으로 글자 내부와 외부를 구분합니다.

텍스트를 확대해도 텍셀에 저장된 거리 정보는 그대로이므로 셰이더가 윤곽선을 정확히 계산할 수 있고 경계 영역에서 부드러운 보간이 이루어져 선명함이 유지되며, 하나의 SDF 텍스처로 모든 크기에 대응할 수 있어 크기 의존성 문제가 사라집니다.

### TextMeshPro의 성능 이점

크기 독립성은 시각 품질에서 멈추지 않고 갱신 비용까지 줄여줍니다.

SDF는 크기 변화와 무관하므로 표시 크기가 달라져도 글리프 메트릭을 다시 계산하지 않고, 텍스트 내용이 바뀔 때도 갱신 경로가 짧아 메쉬 갱신 비용이 낮습니다.

같은 폰트를 여러 크기로 표시해도 텍스처 한 장으로 충분하므로, Legacy Text처럼 크기마다 폰트 텍스처를 새로 만드는 일도 거의 없습니다.

추가 시각 효과의 비용도 낮습니다. SDF가 가진 거리 데이터를 활용해 외곽선(Outline), 그림자(Shadow), 글로우(Glow)를 셰이더 안에서 그려낼 수 있기 때문입니다.

Legacy Text에서 같은 효과를 적용하면 정점을 복제해 메쉬에 덧붙입니다.

Shadow는 원본을 한 번 offset해 깔기 때문에 정점이 두 배가 되고, Outline은 네 모서리 방향으로 각각 복제해 다섯 배까지 늘어나며, 재생성 비용도 그만큼 커집니다.

반면 TextMeshPro는 메쉬를 그대로 둔 채 셰이더 안에서 처리하므로, 효과를 더해도 메쉬 규모는 변하지 않습니다.

<br>

| 항목 | Legacy Text | TextMeshPro |
|------|-------------|-------------|
| 렌더링 방식 | 비트맵 | SDF |
| 확대/축소 | 흐려짐/깨짐 | 선명 유지 |
| 크기별 텍스처 | 크기마다 별도 필요 | 하나로 모든 크기 |
| 외곽선/그림자 | 정점 복제(2~5배) | 셰이더에서 처리 |
| 메쉬 재생성 | 전면 재생성 | 최적화된 재생성 |
| 텍스처 재생성 | 빈번 | 적음 |

<br>

TextMeshPro는 Unity 2018.1부터 패키지 매니저로 제공되었고, Unity 2018.3부터 모든 프로젝트에 기본 포함됩니다.

신규 프로젝트에서 Legacy Text를 사용할 이유는 없습니다.

---

## 폰트 아틀라스 — 한글의 글자 수 문제

SDF 렌더링은 각 글자의 SDF 데이터가 **폰트 아틀라스(Font Atlas)** 에 준비되어 있어야 동작합니다.

폰트 아틀라스는 폰트의 글자들을 하나의 텍스처에 모아 둔 자료 구조로, 스프라이트를 하나의 텍스처에 모으는 스프라이트 아틀라스(Sprite Atlas)와 같은 원리입니다.

그런데 "글자들을 하나의 텍스처에 담는다"는 이 전제는 한글에서 영문과 다른 부담으로 작용합니다.

### 영문과 한글의 차이

영문은 대소문자와 숫자, 기본 기호를 합쳐도 약 100자에 그치므로 512x512 텍스처 하나에 여유 있게 담깁니다.

반면 유니코드 완성형 한글은 초성 19개, 중성 21개, 종성 28개(없음 포함)의 조합으로 **11,172자**에 이릅니다.

이 전부를 하나의 SDF 텍스처에 담으려면 4096x4096 이상의 텍스처와 수십 MB의 메모리가 필요하므로, 같은 "폰트 아틀라스"라도 언어에 따라 규모가 두 자릿수 이상 벌어지는 셈입니다.

### 정적 아틀라스와 동적 아틀라스

한글의 큰 아틀라스 부담을 다루는 핵심은 SDF 데이터를 언제 텍스처에 채우느냐에 있습니다.

**정적 아틀라스(Static Atlas)** 는 빌드 시점에 필요한 글자를 미리 아틀라스에 포함시켜 두는 방식입니다.

런타임에 SDF를 새로 만들지 않으므로 생성 연산 비용은 들지 않지만, 어떤 글자가 사용될지 빌드 전에 파악해 두어야 합니다.

영문처럼 글자 수가 적은 언어라면 전체 문자를 그대로 담아도 부담이 적지만, 한글 11,172자를 전부 포함하면 수십 MB의 텍스처가 그대로 메모리에 상주하게 됩니다.

**동적 아틀라스(Dynamic Atlas)** 는 런타임에 새 글자가 요구되면 그 글자의 SDF 데이터를 만들어 아틀라스 텍스처에 추가하는 방식이며, TextMeshPro에서는 Dynamic SDF 모드로 제공됩니다.

이미 담긴 글자는 그대로 두므로 초기 메모리 사용량은 낮게 유지되지만, 새 글자가 처음 등장할 때마다 CPU에서 SDF 생성 연산이 실행됩니다.

처음 보는 글자가 많이 섞인 채팅 메시지가 한 프레임에 한꺼번에 출력되면, 이 연산이 몰리면서 프레임 지연으로 이어질 수 있습니다.

또한 동적 아틀라스에서는 CPU 연산 외에도 비용이 발생합니다. 아틀라스가 가득 차면 더 큰 텍스처로 확장하거나, 사용 빈도가 낮은 글자를 빼고 남은 글자를 다시 배치해야 하는데, 그때마다 갱신된 텍스처를 GPU로 다시 올리는 업로드 비용이 더해집니다.

결국 정적 아틀라스에는 메모리 부담이, 동적 아틀라스에는 CPU 연산과 텍스처 업로드 비용이 따르므로, 글자의 성격에 따라 두 방식을 섞어 쓰는 전략이 필요합니다.

### 혼합 전략

두 방식을 어떻게 섞을지는 글자의 사용 빈도와 예측 가능성에 달려 있습니다.

정적 아틀라스에는 사전에 사용이 예측되고 자주 등장하는 글자를 담습니다. 숫자와 영문, 기본 기호, 고정 UI 텍스트, 그리고 자주 쓰이는 한글이 여기에 해당하며, 런타임 SDF 생성 부담을 줄여 줍니다.

여기서 "자주 쓰이는 한글"은 보통 KS X 1001 완성형 2,350자를 가리킵니다. 이 범위는 일상적인 한국어 텍스트 대부분을 커버하므로, 2,350자만 정적으로 담아 두면 런타임에 동적으로 추가할 글자 수가 줄어들고 11,172자 전체를 포함할 때보다 메모리 사용량도 적습니다.

반면 동적 아틀라스에는 채팅 메시지나 유저 닉네임처럼 어떤 글자가 나올지 미리 알 수 없는 입력의 드문 글자를 런타임에 추가합니다.

이렇게 두 아틀라스를 함께 쓰면 런타임 SDF 생성 부담과 CPU SDF 생성·텍스처 업로드 비용이 모두 줄어듭니다.

---

## UI 오버드로우 — 같은 픽셀을 여러 번 그리는 비용

Canvas 분리, ScrollRect 풀링, TextMeshPro가 CPU 측 리빌드 비용을 줄이는 전략이었다면, UI 오버드로우는 GPU에서 같은 픽셀을 여러 번 그리는 비용입니다. 반투명 요소가 겹칠수록 이 비용이 커지며, 몇 가지 방법으로 줄일 수 있습니다.

### 반투명 레이어의 겹침

UI 요소는 대부분 **반투명(Alpha)** 을 포함하며, 버튼의 모서리 라운딩, 패널의 반투명 배경, 그림자 효과, 텍스트의 안티앨리어싱이 모두 알파 채널을 사용합니다.

반투명 요소는 뒤에 있는 것이 비쳐 보여야 하므로 깊이 테스트(Depth Test)로 걸러지지 않고, 겹치는 모든 요소가 순서대로 그려져야 합니다. 예를 들어 배경 이미지 위에 반투명 패널, 그 위에 버튼, 그 위에 텍스트가 겹치면, 텍스트 위치의 한 픽셀은 4번 그려집니다(오버드로우 4x).

[GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼 오버드로우는 모바일 GPU에서 특히 비용이 크며, 불투명 오브젝트에서는 하드웨어 최적화가 불필요한 셰이딩을 미리 제거해 줍니다. Mali의 FPK(Forward Pixel Kill), Adreno의 LRZ(Low-Resolution Z), Apple의 HSR(Hidden Surface Removal)이 대표적인 예입니다. 모두 최종적으로 보이지 않을 픽셀을 사전에 판별해 프래그먼트 셰이더 실행을 건너뛰는 기술입니다.

반면 반투명 오브젝트는 이 최적화의 도움을 받지 못합니다. 겹치는 만큼 프래그먼트 셰이더가 실행되며, GPU의 제한된 필레이트(GPU가 초당 처리할 수 있는 픽셀 수) 예산을 소모합니다.

UI는 반투명 요소의 비율이 3D 씬보다 높고 버튼·패널·텍스트·아이콘 대부분이 알파 채널을 포함하므로, UI에서 오버드로우 비용이 쉽게 누적됩니다.

### 오버드로우 줄이기

오버드로우를 줄인다는 것은 최종 화면에 거의 기여하지 않는 프래그먼트 처리를 줄이는 일입니다. 같은 픽셀 위에 여러 UI가 겹치거나, 보이지 않는 UI가 렌더링 대상에 남아 있으면 GPU는 결과적으로 필요 없는 픽셀까지 처리하게 됩니다.

가장 먼저 줄여야 할 것은 완전히 가려진 UI입니다. 메뉴 창처럼 불투명한 패널이 화면을 덮으면, 그 아래의 배경 이미지는 사용자에게 보이지 않습니다. 하지만 UGUI의 UI 요소는 일반적으로 투명 렌더링 경로로 처리되고, 3D 오브젝트처럼 깊이 테스트로 가려진 픽셀이 자동 제거되지 않습니다. 따라서 패널 뒤에 있는 배경 이미지나 장식 요소는 직접 비활성화하거나 렌더링 대상에서 제외해야 합니다.

겹친 UI뿐 아니라 한 장의 이미지 안에서도 낭비가 생깁니다. UI Image는 사각형 메쉬(쿼드)로 렌더링되므로, 실제 그림이 차지하는 영역과 관계없이 쿼드 전체에서 프래그먼트 셰이더가 실행됩니다. 아이콘 주변에 넓은 투명 여백이 있으면, 그 투명 픽셀에서도 텍스처 읽기와 블렌딩 연산이 발생합니다.

알파 값이 0인 픽셀은 최종 색상에는 영향을 주지 않지만, 쿼드 안에 포함되어 있는 한 프래그먼트 처리 자체는 이미 발생합니다. 그래서 스프라이트의 투명 영역을 잘라내어(Trim) 콘텐츠 영역만 남기면 쿼드가 작아지고, 처리해야 할 픽셀 수가 줄어듭니다.

다음으로 확인할 것은 화면에 보이지 않는 UI가 활성화 상태로 남아 있는 경우입니다. 다른 화면에 가려진 팝업이나 숨겨진 패널이 활성화되어 있으면, Unity는 여전히 이들을 렌더링 대상으로 볼 수 있습니다. 이런 요소는 `SetActive(false)`로 끄거나 Canvas 컴포넌트의 `enabled = false`로 렌더링에서 제외할 수 있습니다. 후자는 하위 오브젝트의 `OnEnable`·`OnDisable` 콜백을 일으키지 않고 Canvas 렌더링만 멈추므로, 단순히 화면에서 제외하려는 경우 더 가볍습니다.

화면 전체를 덮는 UI에서는 한 단계 더 나아갈 수 있습니다. 인벤토리나 설정 화면처럼 뒤의 3D 씬이 전혀 보이지 않는 상태라면, 3D 씬을 그리는 카메라 자체를 비활성화할 수 있습니다. 이 경우에는 UI 오버드로우만 줄어드는 것이 아니라 드로우콜, 정점 처리, 조명 계산, 셰도우 맵, 포스트 프로세싱까지 3D 렌더링 파이프라인 전체가 생략됩니다. 픽셀 몇 개를 덜 그리는 최적화가 아니라, 보이지 않는 화면 뒤쪽의 렌더링 패스 자체를 제거하는 최적화입니다.

---

## Raycast Target — 불필요한 입력 처리 제거

오버드로우가 GPU에서 필요 없는 픽셀을 처리하는 문제라면, Raycast Target은 CPU에서 필요 없는 UI 요소를 검사하는 문제입니다. 화면에 그려지는 모든 UI가 입력을 받아야 하는 것은 아니므로, 실제 상호작용 대상만 검사 후보로 남기는 것이 중요합니다.

### Raycast Target의 역할

Unity UGUI에서 터치나 클릭 입력이 발생하면, **GraphicRaycaster**가 입력 위치와 겹치는 UI 요소를 찾습니다. 이때 검사 대상이 되는 것은 **Raycast Target** 속성이 켜져 있는 Graphic 요소입니다.

예를 들어 배경 이미지, 프레임, 장식 아이콘, 텍스트 라벨, 버튼, 스크롤바가 모두 Raycast Target을 켜고 있다면 6개 전부가 검사 후보가 됩니다. 하지만 실제로 입력을 받아야 하는 것은 버튼과 스크롤바뿐입니다. 나머지 요소는 화면에 보이기만 하면 되므로, 입력 검사에 참여할 필요가 없습니다.

### 기본값의 문제

문제는 Unity의 Image, Text(Legacy), TextMeshPro 같은 Graphic 컴포넌트가 생성될 때 Raycast Target이 기본으로 **켜져** 있다는 점입니다. 버튼이나 슬라이더처럼 입력을 받아야 하는 요소에는 필요한 설정이지만, 배경 이미지나 텍스트 라벨처럼 표시만 하는 요소에는 불필요합니다.

UI 요소가 수십~수백 개인 화면에서 대부분의 요소가 Raycast Target을 유지하면, 터치 이벤트마다 실제 입력 대상이 아닌 요소까지 겹침 검사에 포함됩니다.

모바일 입력은 한 번의 터치도 다운, 무브, 업 같은 여러 이벤트로 나뉘어 처리됩니다. 따라서 검사 후보가 많을수록 작은 비용이 여러 번 반복되고, UI가 복잡한 화면에서는 누적 비용이 커집니다.

### Raycast Target을 꺼야 하는 요소

Raycast Target은 실제로 입력을 받아야 하는 요소에만 남기는 것이 좋습니다. 버튼, 슬라이더, 토글, 입력 필드, ScrollRect, 드래그 가능한 요소처럼 상호작용이 필요한 요소는 유지하고, 배경 이미지, 장식 프레임, 텍스트 라벨, 표시용 아이콘처럼 보여 주기만 하는 요소는 끕니다.

버튼 안의 자식 텍스트도 대부분 끌 수 있습니다. 버튼 이미지나 Button 컴포넌트가 붙은 Graphic이 터치 영역을 담당하므로, 그 위에 올라간 텍스트까지 별도의 검사 대상이 될 필요는 없습니다.

---

## 전략의 조합

지금까지 다룬 전략들은 모두 UI 비용을 줄이지만, 줄이는 대상은 서로 다릅니다. Canvas 분리는 리빌드 범위를 줄이고, ScrollRect 풀링은 생성해 두어야 하는 UI 오브젝트 수를 줄입니다. TextMeshPro와 폰트 아틀라스 전략은 텍스트 렌더링과 폰트 텍스처 비용을 관리하고, 오버드로우 감소는 GPU의 프래그먼트 처리량을 줄입니다. Raycast Target 관리는 입력 이벤트마다 발생하는 CPU 검사를 줄입니다.

따라서 하나의 방법으로 모든 UI 성능 문제를 해결하려 하기보다, 화면에서 실제로 비용이 발생하는 위치에 맞춰 조합해야 합니다. 자주 갱신되는 HUD는 Canvas 분리가 우선이고, 긴 리스트는 풀링 효과가 큽니다. 반투명 레이어가 많이 겹친 화면은 오버드로우를 확인해야 하며, 상호작용하지 않는 장식 요소가 많은 화면은 Raycast Target 정리가 도움이 됩니다.

각 전략이 건드리는 병목이 다르기 때문에, 서로 충돌하기보다 함께 적용될 때 효과가 누적됩니다.

---

## 마무리

- Canvas 분리는 자주 변하는 요소와 변하지 않는 요소를 나누어, 불필요한 Canvas 리빌드를 줄입니다.
- ScrollRect 풀링은 화면에 보이는 만큼의 아이템만 유지하여, 긴 리스트의 오브젝트 수와 리빌드 부담을 줄입니다.
- TextMeshPro는 SDF 기반 렌더링으로 텍스트 품질을 유지하면서, Legacy Text보다 낮은 메쉬 재생성 비용을 가집니다.
- 한글 UI에서는 자주 쓰는 글자를 정적 아틀라스에 담고, 예측하기 어려운 글자는 동적 아틀라스로 처리해 폰트 텍스처 비용을 조절합니다.
- 오버드로우는 가려진 UI, 넓은 투명 영역, 불필요한 배경 렌더링을 줄여 프래그먼트 처리량을 낮춥니다.
- Raycast Target은 실제로 입력을 받아야 하는 요소에만 남겨, 터치 이벤트마다 발생하는 겹침 검사를 줄입니다.

UI는 대부분의 프레임에서 항상 화면에 남아 있습니다. 따라서 작은 리빌드, 픽셀 처리, 입력 검사 비용도 방치하면 매 프레임 누적되고, 모바일에서는 곧바로 프레임 예산을 압박합니다.

<br>

---

**관련 글**
- [Unity의 Layout Update Cycle](/dev/unity/UnityLayoutUpdateCycle/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- **UI 최적화 (2) - UI 최적화 전략** (현재 글)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- **UI 최적화 (2) - UI 최적화 전략** (현재 글)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
