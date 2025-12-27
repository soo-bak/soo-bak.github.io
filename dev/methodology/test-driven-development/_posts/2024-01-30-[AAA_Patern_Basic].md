---
layout: single
title: "AAA패턴 : TDD 의 핵심 원칙 - soo:bak"
date: "2024-01-30 00:03:00 +0900"
description: "TDD의 핵심 원칙인 AAA 패턴(Arrange-Act-Assert)을 C++, C# 예제와 함께 상세히 설명합니다."
tags:
  - TDD
  - AAA 패턴
  - 단위 테스트
  - C#
  - C++
  - 소프트웨어 개발
keywords: "AAA 패턴, Arrange Act Assert, TDD, 테스트 주도 개발, 단위 테스트, C#, C++"
---
<br>

## AAA 패턴 : 테스트 주도 개발(TDD) 의 핵심 원칙
`AAA 패턴` 은 `테스트 주도 개발(TDD)` 에서 자주 사용되는 중요한 테스트 작성 원칙 중 하나이다.<br>
<br>
이 패턴을 이해하고 활용함으로써, 효과적인 테스트 케이스를 작성하고 코드를 안정적으로 개발하는 데 도움을 얻을 수 있다.<br>
<br>
`AAA 패턴` 은 다음의 세 가지 요소로 구성된다.
<br><br><br>

### `Arrange` - 준비
`Arrange` 단계에서는 테스트 환경을 설정하는 일을 한다.<br>
<br>
이 단계에서는 테스트에 필요한 <b>초기화 작업</b>을 수행하고, 테스트 대상 객체를 생성하거나 설정한다.<br>
<br>
이 단계에서 해야 할 일은 다음과 같다 :<br>
<br><br>
- 테스트에 필요한 객체, 변수, 또는 데이터를 생성하고 준비한다.<br>
<br>
- 테스트 대상 객체를 초기화하거나 설정한다.<br>
<br>
- 필요한 상태나 조건을 설정한다.<br>
<br><br>

예를 들어, '정수 덧셈 함수' 를 테스트한다고 가정했을 때, 이 함수를 테스트하기 위해서는 두 개의 정수 값을 설정하고, 덧셈 함수에 전달해야 한다.<br>
<br>
이 과정이 `Arrange` 단계에 해당한다.<br>
<br><br>

### `Act` - 실행
`Act` 단계에서는 테스트 대상 코드를 호출하거나 실행한다.<br>
<br>
즉, 테스트하려는 동작을 실제로 수행하는 부분이다.<br>
<br>
이 단계에서는 `Arragne` 단계에서 준비한 환경과 데이터를 사용하여 테스트 대상 코드를 호출하고, 그 결과를 얻는다.<br>
<br><br>

예를 들어, '정수 덧셈 함수' 를 테스트하는 경우, 이 함수를 호출하고 그 값을 얻어내는 것이 `Act` 단계에 해당한다.<br>
<br><br>

### `Assert` - 단언
`Assert` 단계에서는 `Act` 단계에서 실행한 코드의 결과를 검증하고, 예상한 대로 동작하는지 확인한다.<br>
<br>
이 단계에서 테스트가 성공적으로 통과되었는지 여부를 판단하게 된다.<br>
<br><br>

예를 들어, 정수 덧셈 함수를 테스트한 후, 결과 값을 검증하여 예상한 결과와 일치하는지 확인하는 것이 `Assert` 단계에 해당한다.<br>
<br>
결과가 예상한 대로면 테스트는 통과하고, 그렇지 않으면 테스트는 실패한다.<br>
<br><br><br>

## AAA 패턴의 장점
`AAA` 패턴을 사용하면 테스트 작성과 관리가 더욱 효과적으로 이루어진다.<br>
<br>
이 패턴을 따르면, 다음과 같은 이점을 얻을 수 있다 :<br>
<br>
<b>1. 가독성 향상 </b><br>
<br>
각 단계가 명확하게 구분되므로, 다른 개발자들이 테스트 코드를 더 쉽게 이해하고 따라갈 수 있다.<br>
<br><br>
<b>2. 유지보수성 향상</b><br>
<br>
각 단계가 분리되어 있으므로 변경 또는 확장이 필요한 경우 해당 단계만 수정하면 된다.<br>
<br>
<b>3. 버그 식별 용이성</b><br>
<br>
`Assert` 단계에서 예상한 결과와 다른 경우, 문제를 더 쉽게 파악할 수 있다.<br>
<br>
<b>4. 자동화 용이</b><br>
<br>
`AAA` 패턴을 따르면 테스트 케이스를 자동화하기 더 쉽다.<br>
<br>
이는 지속적인 통합 및 자동화 테스트에 매우 유용하다.<br>
<br><br><br>

## 예시

### 예시 - 두 정수 덧셈 함수
<br>

<b>[C++]</b>
<br>

```c++
#include <iostream>

using namespace std;

// 정수 덧셈 함수
int add(int a, int b) {
  return a + b;
}

// 테스트 케이스 작성
void testAddition() {
  // Arrange
  int num1 = 5;
  int num2 = 3;

  // Act
  int result = add(num1, num2);

  // Assert
  if (result == 8)
    cout << "테스트 통과!" << endl;
  else
    cout << "테스트 실패!" << endl;
}

int main() {
  testAddition();

  return 0;
}
```

<br><br>
<b>[C#]</b>
<br>

```c#
using System;

// 정수 덧셈 함수
public class Calculator {
  public static int Add(int a, int b) {
    return a + b;
  }
}

// 테스트 케이스 작성
public class TestCalculator {
  public static void TestAddition() {
    // Arrange
    int num1 = 5;
    int num2 = 3;

    // Act
    int result = Calculator.Add(num1, num2);

    // Assert
    if (result == 8)
      Console.WriteLine("테스트 통과!");
    else
      Console.WriteLine("테스트 실패!");
  }

  public static void Main() {
    TestAddition();
  }
}
```
<br><br><br>

### 예시 - 문자열 뒤집기 함수
<br>

<b>[C++]</b>
<br>

```c++
#include <iostream>
#include <vector>

using namespace std;

// 간단한 문자열 뒤집기 함수
string reverseString(const string& input) {
  string reversed;
  for (int i = input.length() - 1; i >= 0; --i)
    reversed += input[i];

  return reversed;
}

// 테스트 케이스 작성
void testReverseString() {
  // Arrange
  string input = "Hello, World!";
  string expected = "!dlroW ,olleH";

  // Act
  string result = reverseString(input);

  // Assert
  if (result == expected) cout << "테스트 통과!" << endl;
  else cout << "테스트 실패!" << endl;
}

int main() {
  testReverseString();

  return 0;
}
```

<br><br>
<b>[C#]</b>
<br>

```c#
using System;

// 간단한 문자열 뒤집기 함수
public class StringManipulator {
  public static string ReverseString(string input) {
    var charArray = input.ToCharArray();
    Array.Reverse(charArray);
    return new string(charArray);
  }
}

// 테스트 케이스 작성
public class TestStringManipulator {
  public static void TestReverseString() {
    // Arrange
    string input = "Hello, World!";
    string expected = "!dlroW ,olleH";

    // Act
    string result = StringManipulator.ReverseString(input);

    // Assert
    if (result == expected)
      Console.WriteLine("테스트 통과!");
    else
      Console.WRiteLine("테스트 실패!");
  }

  public static void Main() {
    TestReverseString();
  }
}
```
<br><br><br>

## 마무리
`AAA` 패턴은 `테스트 주도 개발(TDD)` 에서 핵심적인 역할을 하는 테스트 작성 원칙 중 하나이다.<br>
<br>
이 패턴을 따르면, 테스트 코드를 명확하게 작성하고 코드의 동작을 신뢰성 있게 검증할 수 있다.<br>
<br>
이를 통해, 소프트웨어의 품질을 향상시키고 버그를 최소화하는데 도움을 얻을 수 있다.<br>
<br>
<br>
<br>
