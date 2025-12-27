---
layout: single
title: "[백준 14337] Helicopter (VisualBasic) - soo:bak"
date: "2023-05-03 23:11:00 +0900"
description: VisualBasic 으로 출력을 하는 백준 14337번 문제 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 14337
  - 알고리즘
keywords: "백준 14337, 백준 14337번, BOJ 14337, 알고리즘"
---

## 문제 링크
  [14337번 - Helicopter](https://www.acmicpc.net/problem/14337)

## 설명
아스키 문자를 출력하는 간단한 문제이지만, 제출할 수 있는 언어가 `VisualBasic` 으로 제한되어 있습니다. <br>

`VisualBasic` 언어에 대한 간단한 설명은 다음과 같습니다. <br>
- 마이크로소프트(Microsoft)에서 개발한 언어로, 프로그래밍 초보자가 쉽게 접근할 수 있는 도구로 설계 <br>
- 개발자들이 빠르게 Windows 기반의 응용 프로그램들을 만들 수 있도록 지원<br>
- 마지막 버전인 `VisualBasic 6.0` 은 1998년도에 출시되었으며, 이후에는 `VB.NET` 으로 진화 <br>
- 이후, `.NET` 프레임워크를 기반으로 한 새로운 버전이 만들어지고, `VisualBasic` 은 점차 `VB.NET` 으로 대체<br>
- `VB.NET` 은 객체지향 프로그래밍 기능을 강화하고, `.NET` 프레임워크와의 호환성을 높임 <br>

즉, 기존 `BASIC` 언어 사용자들이 현대 프로그래밍 환경에 적응하는 데 도움이 되는 언어라고 합니다. <br>

<br>

아래 코드에서 사용한 `VisualBasic` 의 문법에 대한 설명은 다음과 같습니다.<br>
코드 라인의 순서대로 설명하겠습니다. <br>

- `Module Helicopter` : 새로운 코드 모듈을 선언하고, 해당 모듈의 이름을 지정합니다. <br>
- `Sub Main()` : `Main` 이라는 이름의 새로운 서브루틴을 선언합니다. 이는 프로그램 실행의 시작점이 됩니다. <Br>
- `Console.Writeline()` : 콘솔 창에 문자열을 출력하며, 마지막에 개행 문자를 자동으로 출력합니다. <br>
- `End Sub` : `Main` 서브루틴의 끝을 나타냅니다. <br>
- `End Module` : `Helicopter` 모듈의 끝을 나타냅니다. <br>

<br>
- - -

## Code
<b>[ VisualBasic ] </b>
<br>

  ```VisualBasic
Module Helicopter
    Sub Main()
        Console.WriteLine("      ===================")
        Console.WriteLine("          ____||___")
        Console.WriteLine("\ /      /       []\")
        Console.WriteLine(" X=======           \__")
        Console.WriteLine("/ \      \____________|")
        Console.WriteLine("            ||  ||")
        Console.WriteLine("         \-----------/")
    End Sub
End Module
  ```
