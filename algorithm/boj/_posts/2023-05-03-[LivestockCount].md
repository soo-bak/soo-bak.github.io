---
layout: single
title: "[백준 2372] Livestock Count (Ada) - soo:bak"
date: "2023-05-03 21:33:00 +0900"
description: Ada 언어의 출력을 주제로 하는 백준 2372번 알고리즘 문제의 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2372
  - 알고리즘
keywords: "백준 2372, 백준 2372번, BOJ 2372, 알고리즘"
---

## 문제 링크
  [2372번 - Livestock Count](https://www.acmicpc.net/problem/2372)

## 설명
아스키 문자를 출력하는 간단한 문제이지만, 제출할 수 있는 언어가 `Ada` 로 제한되어 있습니다. <br>

`Ada` 언어에 대한 간단한 설명은 다음과 같습니다. <br>
- `1970` 년대 후반에 개발된 고급 프로그래밍 언어로, 알고리즘 설계 및 시스템 설계에 사용됨 <br>
- 특히, 안정성과 신뢰성, 정확성이 중요한 시스템에서 사용됨 <br>
- 미국 국방성(DoD)의 요청으로 개발되었으며, 19세기 초의 영국 수학자인 `Ada Lovelace` 에서 이름을 따옴 <br>
- 강력한 타입 시스템으로 프로그램의 안정성과 신뢰성 향상 <br>
- 타입 간의 변환은 반드시 명시적으로 수행하여야 함 <br>
- 병렬 프로그래밍 지원 <br>
- 명확하고 가독성 있는 문법으로 코드 이해와 유지 보수가 용이 <br>
<br>

`Ada` 는 항공 교통 제어, 군사 시스템, 위성 제어, 철도 시스템 등과 같이 신뢰성이 매우 중요한 분야에서 주로 사용된다고 합니다. <br>
그러나 `Ada` 의 복잡성과 습득 곡선으로 인하여, 현재는 다른 프로그래밍 언어들에 비하여 비교적 덜 널리 사용되고 있다고 합니다. <br>
<br>

아래 코드에서 사용한 `Ada` 의 문법에 대한 설명은 다음과 같습니다.<br>
코드 라인의 순서대로 설명하겠습니다. <br>

- `with Ada.Text_IO;` : `Ada` 의 표준 입출력 라이브러리인, `Ada.Text.IO` 를 `with` 키워드를 통해 가져옵니다.<br>
- `use Ada.Text_IO` : `use` 키워드를 통해 `Ada.Text.IO` 라이브러리를 사용합니다. <br>
- `Procedure Livestock_Count is` : 새로운 프로시저(procedure)를 정의합니다. `is` 키워드는 프로시저의 본문이 시작됨을 나타냅니다. <br>
- `begin` : `begin` 키워드는 프로시저의 본문이 시작됨을 나타냅니다. <br>
- `put_line ()` : `put_line` 은 `Ada.Text_IO` 라이브러리의 함수로, 문자열을 출력한 후 줄바꿈을 수행하는 기능을 합니다. <br>
- `end Livestock_Count;` : `end` 키워드는 프로시저 본문의 종료를 나타내며, 뒤에 프로시저의 이름이 따라오고 세미콜론 `;` 으로 끝을 맺습니다. <br>

<br>
- - -

## Code
<b>[ Ada ] </b>
<br>

  ```Ada
with Ada.Text_IO; use Ada.Text_IO;

procedure Livestock_Count is
begin
   Put_Line ("Animal      Count");
   Put_Line ("-----------------");
   Put_Line ("Chickens      100");
   Put_Line ("Clydesdales     5");
   Put_Line ("Cows           40");
   Put_Line ("Goats          22");
   Put_Line ("Steers          2");
end Livestock_Count;
  ```
