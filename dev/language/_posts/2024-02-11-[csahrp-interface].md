---
layout: single
title: "C# 에서의 인터페이스(Interface) - soo:bak"
date: "2024-02-12 01:27:00 +0900"
description: "C# 인터페이스의 개념, 선언 방법, 장점을 설명합니다. 다형성, 다중 상속과의 관계를 다룹니다."
tags:
  - C#
  - 인터페이스
  - Interface
  - OOP
  - 다형성
keywords: "C# 인터페이스, Interface, 다형성, 다중 상속, OOP, 객체지향 프로그래밍"
---
<br>

## 인터페이스(Interface)
`인터페이스` 는 일종의 '명세' 와 같다.<br>
<br>
`인터페이스` 클래스 자체는 멤버의 <b>구현</b>을 포함하지 않으며, 오직 <b>선언</b>만 포함한다.<br>
<br>
즉, 인터페이스를 상속받는 클래스나 구조체가 <b>구현</b>해야하는 멤버들에 대해서, <b>선언</b>만을 통해 '명세' 하는 역할을 한다.<br>
<br>
이를 통해 객체 지향의 '다형성' 을 구현할 수도 있으며, 코드의 유연성과 재사용성을 크게 향상시킬 수 있다.<br>
<br>

## C# 에서의 인터페이스(Interface)
`C#` 에서는 인터페이스를 `interface` 키워드를 사용하여 선언한다.<br>
<br>

<b>[예시]</b><br>

```c#
interface IInterfaceName {
  // 속성 정의
  int Property {get; set; }

  // 메서드 정의
  void Method();

  // 이벤트 정의
  event EventHanlder Event;
}
```
<br>
이 때, `C#` 에서의 `인터페이스`는 `클래스`와 다르게, 메서드, 이벤트, 인덱서, 프로퍼티만을 멤버로 가질 수 있으며, 해당 멤버들에 대한 구현 부분이 존재하지 않는다.<br>
<br>
또한, 인터페이스는 접근 제한 지정자를 사용할 수 없으며, 모든 것이 <u>암묵적으로</u> `public` 으로 선언된다.<br>
<br>
인터페이스를 상속 받는 파생 클래스는, 인터페이스에 선언된 모든 메서드 및 프로퍼티를 구현하여야 하며, 이 멤버들은 `public` 한정자로 수식해주어야 한다.<br>
<br>

<b>[예시]</b><br>

```c#
class MyClass : IInterfaceName {
  public int Property { get; set; }

  public void Method {
    // 메서드 구현
  }

  public event EventHandler Event;
}
```
<br>
<br>
<br>

## 인터페이스의 장점
<b>다형성</b>
<br>: `인터페이스`를 통해, 다양한 `클래스`를 '동일한 인터페이스'로 참조 할 수 있다.<br>
<br>
이러한 방법을 통해 객체 지향의 '다형성' 을 구현할 수 있다.<br>
> 참고 : [다형성(Polymorphism) - soo:bak](https://soo-bak.github.io/dev/programming-paradigm/object-oriented-programming/Polymorphism/)

<br>

<b>모듈성과 결합도 감소</b>
<br>: `인터페이스` 는 '구현' 을 분리하여 모듈성을 향상시키고, 클래스 간의 결합도를 감소시킨다.<br>
<br>
<br>

<b>계약에 의한 프로그래밍</b>
<br>: `인터페이스` 는 `클래스` 의 외부 계약을 정의한다.<br>
<br>
이 때, `클래스`는 `인터페이스` 에 정의된 계약을 준수해야 하므로, <b>인터페이스를 통해 명확한 `API` 를 제공</b>할 수 있다.<br>
<br>
<br>

<b>다중 상속</b>
<br>: `C#` 에서는 `클래스` 의 '다중 상속' 을 지원하거나 허용하지 않는다.<br>
<br>
하지만, `인터페이스` 의 '다중 상속' 은 허용한다.<br>
<br>
이는 `인터페이스` 가 '내용' 이 아닌 '외형' 에 대해 강제를 하는 의미를 가지고 있기 때문에, <b>구현에 대한 모호성 문제가 없기 때문</b>이다.<br>
<br>
즉, 인터페이스의 다중 상속에서는 '죽음의 다이아몬드(DDD, the Deadly Diamond of Death)', 'Up-casting 에서의 모호성' 등의 문제가 생기지 않기 때문에, 다중 상속이 허용되는 것이다.<br>
> 참고 : [죽음의 다이아몬드(DDD, the Deadly Diamond of Death) - soo:bak](https://soo-bak.github.io/dev/programming-paradigm/object-oriented-programming/DeadlyDiamondofDeath/)

<br>
<br>
<br>

## 인터페이스 사용의 주의점
- 인터페이스는 '구현' 을 포함할 수 없으며, 모든 멤버는 구현 클래스에서 정의되어야 한다.<br>
<br>
- 인터페이스 멤버들은 기본적으로 `public` 이므로, 인터페이스를 구현하는 클래스는 해당 멤버들을 `public` 접근 지정자로 선언해야 한다.<br>
<br>
<br>

### "인터페이스는 인스턴스를 생성할 수 없지만, 참조는 생성 가능하다."
인터페이스 자체는 '구현' 을 포함하지 않는다.<br>
<br>
따라서, 인터페이스로부터 직접 인스턴스를 생성할 수는 없다.<br>
<br>
<br>
즉, 다음의 코드에서 : <br>
<br>

```c#
public interface ILogger {
  void WriteLog(string message);
}
```
<br>

아래와 같은 코드는 컴파일 에러를 발생시킨다.

```c#
ILogger logger = new Ilogger();
```
<br>

그러나, 인터페이스를 구현하는 클래스의 객체로 인터페이스 타입의 참조를 생성할 수 있고,<br>
<br>
이러한 방식으로 인터페이스는 다형성을 지원하게 된다.<br>
<br>

```c#
public class ConsoleLogger : ILogger {
  public void WriteLog(string message) {
    Console.WriteLine(message);
  }
}
```
<br>
위 코드에서, `ConsoleLogger` 클래스는 `ILogger` 인터페이스를 구현한다.<br>
<br>
따라서, `ConsoleLogger` 의 `인스턴스` 는 `ILogger` 타입의 `참조`로 참조될 수 있다.<br>
<br>
<br>

```c#
ILogger logger = new ConsoleLogger();
logger.WriteLog("SOOBAK");
```
<br>
위 코드에서, `new ConsoleLogger()` 는 `ConsoleLogger` 클래스의 인스턴스를 생성한다.<br>
<br>
그리고, `ILogger logger` 는 이 인스턴스를 참조하는 `ILogger` 타입의 참조를 생성한다.<br>
<br>
<br>
<br>
인터페이스 참조를 통해, 다양한 구현을 추상화하고, 런 타임에 어떤 구현이 사용될지 결정할 수 있다.<br>
<br>
즉, `C#` 에서 `interface` 키워드를 통한 인터페이스는 `추상화` 와 `다형성` 을 제공하며,<br>
<br>
<u>인스턴스를 직접 생성할 수는 없지만</u>, 인터페이스 타입의 참조를 통해서 다양한 구현에 접근할 수 있다.<br>
<br>
<br>
<br>
