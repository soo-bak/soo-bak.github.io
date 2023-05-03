---
layout: single
title: "[백준 14337] Helicopter (VisualBasic) - soo:bak"
date: "2023-05-03 23:11:00 +0900"
---

## 문제 링크
  [14337번 - Helicopter](https://www.acmicpc.net/problem/14337)

## 설명
아스키 문자를 출력하는 간단한 문제이지만, 제출할 수 있는 언어가 `FreeBASIC` 로 제한되어 있습니다. <br>

`FreeBASIC` 언어에 대한 간단한 설명은 다음과 같습니다. <br>
- `BASIC` 언어의 현대적인 오픈소스 버전 <br>
- 기존 `BASIC` 언어 사용자들이 쉽게적응할 수 있는 구문을 제공하면서도, 현대적인 프로그래밍 언어의 다양한 기능을 제공 <br>
- 초보자가 배우기 쉬운 간결하고 이해하기 쉬운 문법을 제공 <br>
- `Windows`, `Linux`, `DOS` 등 다중 운영체제 지원 <br>

즉, 기존 `BASIC` 언어 사용자들이 현대 프로그래밍 환경에 적응하는 데 도움이 되는 언어라고 합니다. <br>

<br>

아래 코드에서 사용한 `FreeBASIC` 의 문법에 대한 설명은 다음과 같습니다.<br>
코드 라인의 순서대로 설명하겠습니다. <br>

- `Sub Main()` : `Main` 이라는 이름의 서브루틴을 정의합니다. 이 서브루틴은 프로그램이 시작되는 지점입니다. <br>
- `Print` : `FreeBasic` 에서 사용하는 출력 명령어로, 변수와 문자열, 숫자 등을 콘솔 창에 출력하는 데에 사용되며, 출력 후 개행이 됩니다. <Br>
- `End Sub` : `FreeBasic` 에서 서브루틴의 끝을 표시하는 키워드 입니다. <br>
- `Main()` : 프로그램의 실행을 시작하기 위해 `Main` 서브루틴을 호출합니다. <br>

<br>
- - -

## Code
<b>[ FreeBasic ] </b>
<br>

  ```FreeBasic
Sub Main()
    Print " _________"
    Print " \_     _/"
    Print "   \   /"
    Print "    | |"
    Print "   /   \"
    Print "  /     \"
    Print " |       |"
    Print "/---------\"
    Print "| \-/ \-/ |"
    Print "\---------/"
    Print " \_______/"
End Sub

Main()
  ```
