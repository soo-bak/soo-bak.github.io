---
layout: single
title: "- soo:bak"
date: "2024-01-30 00:03:00 +0900"
---
<br>

## 단위 테스팅
단위 테스트는 소프트웨어 개발의 중요한 요소 중 하나이다.<br>
<br>
코드의 격리된 부분을 테스트함으로써, 개발자는 더 견고하고 신뢰할 수 있는 프로그램을 만들 수 있다.<br>
<br>
이러한 과정에서, <b>모의 객체(mock objects)</b> 또는 `mocks` 의 사용은 필수불가결한데, 이는 <u>복잡한 의존성</u>을 가진 코드를 테스트할 때 특히 중요하다.<br>
<br>
`.NET` 환경에서 `NSubstitute` 는 이러한 목적을 위해 널리 사용되는 프레임워크 중 하나이다.<br>
<br><br><br>

## NSubstitute 소개
`NSubstitute` 는 `.NET` 언어 (`C#`, `VB.NET` 등) 를 위한 강력하면서도 사용하기 쉬운 모의 객체 라이브러리이다. <br>
<br>
단위 테스트를 작성할 때, `NSubstitute` 를 사용하면, 실제 구현 대신 `인터페이스` 나 `클래스` 의 <b>가짜 버전</b> 을 쉽게 생성할 수 있다.<br>
<br>
이렇게 하면, 테스트하고자 하는 코드의 특정 부분에 집중할 수 있으며, 외부 시스템, 데이터베이스 호출, 복잡한 클래스 등에 대한 의존성 없이 코드를 검증할 수 있다.<br>
<br><br><br>

## 기본 사용법

### 가짜 객체 생성
`NSubstitute` 를 사용하여 가짜 객체를 생성하는 것은 매우 간단하다.<br>
<br>
예를 들어, `IOrder` 인터페이스에 대한 가짜 객체를 생성하려면 다음과 같이 한다 : <br>
<br>
```c#
var order = Substitute.For<IOrder>();
```
<br>
이 한 줄의 코드로, `NSubstitute` 는 `IOrder` 인터페이스를 구현하는 가짜 객체를 자동으로 생성한다.<br>
<br><br>

### 메서드 동작 설정
가짜 객체의 메서드가 호출될 때, 원하는 동작을 설정할 수 있다.<br>
<br>
예를 들어, `GetOrderName()` 메서드가 `"Test Order"` 이라는 문자열을 반환하도록 설정할 수 있다 : <br>
<br>
```c#
order.GetOrderName().Returns("Test Order");
```
<br>
이 설정을 통해 `GetOrderName()` 메서드가 호출될 때마다, `"Test Order"` 문자열이 반환된다.<br>
<br><br>

### 호출 검증
`NSubstitute` 를 사용하면 특정 메서드가 호출되었는지, 몇 번 호출되었는지 등을 검증할 수 있다.<br>
<br>
예를 들어, `Submit()` 메서드가 한 번 호출되었는지 확인하려면 다음과 같이 한다 : <br>
<br>
```c#
order.Received(1).Submit();
```
<br>
이 코드는 `Submit()` 메서드가 정확히 한 번 호출되었음을 검증한다.<br>
<br><br><br>

## 고급 사용법

### 인수 매칭
`NSubstitute` 는 메서드 호출 시 전달되는 인수를 기반으로 동작을 설정하거나 검증할 수 있는 기능을 제공한다.<br>
<br>
예를 들어, `GetOrderById(int id)` 메서드가 특정 `ID` 에 대해, 특정 동작을 하도록 설정할 수 있다 : <br>
<br>
```c#
order.GetOrderById(Arg.Is(42)).Returns("Special Order");
```
<br>
이 코드는 `GetOrderById()` 메서드에 `42` 가 인수로 전달될 때, `"Special Order"` 을 반환하도록 설정한다.<br>
<br><br>

### 예외 발생 설정
테스트 중에 메서드가 특정 조건에서 예외를 발생시키는 것을 시뮬레이션하고 싶을 때, `NSubstitute` 는 이를 쉽게 설정할 수 있게 해준다 : <br>
<br>
```c#
order.When(x => x.Submit()).Do(x => { throw new Exception("Error"); });
```
<br>
이 설정을 통해 `Submit()` 메서드가 호출될 때마다 지정된 예외가 발생한다.<br>
<br><br>

### 이벤트 구독 및 발생
`NSubstitute` 를 사용하면 가짜 객체의 이벤트에 대한 구독 및 이벤트 발생도 시뮬레이션할 수 있다. <br>
<br>
예를 들어, `OrderProcessed` 이벤트에 대한 구독과 이벤트 발생을 다음과 같이 설정할 수 있다 :
<br>
```c#
//이벤트 구독
order.OrderProcessed += (sender, args) => { /* 이벤트 핸들러 코드 */ };

// 이벤트 발생 시뮬레이션
order.OrderProcessed += Raise.EventWith(new object(), new EventArgs());
```
<br>
이 방법을 통해 이벤트가 발생했을 때의 코드 동작을 테스트할 수 있다.<br>
<br><br><br>

## 결론
`NSubstitute` 는 `.NET` 개발자들에게 단위 테스팅을 위한 강력한 도구를 제공한다.<br>
<br>
이를 통해, 복잡한 의존성을 가진 코드를 쉽게 <b>격리하여</b> 테스트할 수 있으며, 코드의 견고성과 신뢰성을 향상시킬 수 있다.<br>
<br>
가짜 객체 생성부터 고급 기능에 이르기까지, `NSubstitute` 는 단위 테스트의 효율성과 효과성을 크게 높여준다.<br>
<br>
<br>
<br>
