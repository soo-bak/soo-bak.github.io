---
layout: single
title: "다형성(Polymorphism) - soo:bak"
date: "2024-02-12 00:29:00 +0900"
description: "객체지향의 핵심 개념인 다형성을 설명합니다. 오버로딩과 오버라이딩의 차이, C++/C# 예제를 다룹니다."
tags:
  - OOP
  - 다형성
  - Polymorphism
  - 오버로딩
  - 오버라이딩
  - C#
  - C++
keywords: "다형성, Polymorphism, 오버로딩, 오버라이딩, OOP, 객체지향 프로그래밍, C#, C++"
---
<br>

## 다형성(Polymorphism)
`다형성` 은 객체 지향 프로그래밍의 주요 개념 중 하나로, <b>'많은 형태를 가질 수 있는 능력'</b> 을 의미한다.<br>
<br>
<br>
<br>

## 다형성의 개념
다형성은 하나의 `인터페이스` 나 `기반 클래스` 가 여러 형태의 `구현` 을 가질 수 있도록 한다.<br>
<br>
이는 같은 함수 호출에 대해서, <b>호출되는 객체의 타입</b>에 따라 '다른 동작' 을 할 수 있다는 것이다.<br>
<br>
<br>

### 컴파일 타임 다형성 구현 (오버로딩, Overloading)
컴파일 타임 다형성은 함수(메서드) `오버로딩` 을 통해 구현된다.<br>
<br>
즉, <b>같은 이름을 가진 함수(메서드)가 다른 매개변수 리스트(타입, 개수, 순서)를 가질 수 있도록</b> 한다.<br>
<br>
컴파일 타임 다형성은 컴파일 시에 결정되기 때문에,<br>
<br>
컴파일러는 함수(메서드)를 호출할 때 제공된 인수에 기반하여 어떤 함수(메서드) 버전을 호출할지 결정한다.<br>
<br>

<b>[예시 - C++]<br></b>

```c++
#include <iostream>
using namespace std;

class DisplayOverload {
  public:
    void display() {
      cout << "Display without parameters" << endl;
    }

    void display(int i) {
      cout << "Display with integer : " << i << endl;
    }

    void display(const string& s) {
      cout << "Display with string : " << s << endl;
    }
};

int main() {
  DisplayOverload obj;

  obj.display();
  obj.display(101);
  obj.display("SOOBAK");

  return 0;
}
```
<br>

<b>[예시 - C#]<br></b>

```c#
using System;

public class DisplayOverload {
  public void Display() {
    Console.WriteLine("Display without parameters");
  }

  public void Display(int i) {
    Console.WriteLine($"Display with integer : {i}");
  }

  public void Display(string s) {
    Console.WriteLine($"Display with string : {s}");
  }
}

class Program {
  static void Main() {
    DisplayOverload obj = new DisplayOverload();

    obj.Display();
    obj.Display(101);
    obj.Display("SOOBAK");
  }
}
```
<br>
<br>

### 런 타임 다형성 구현 (오버라이딩, Overriding)
런 타임 다형성은 함수(메서드) `오버라이딩` 을 통해 구현된다.<br>
<br>
파생 클래스가 기반 클래스의 함수(메서드)를 '재정의'하여,<br>
<br>
동일한 함수(메서드)를 호출하지만 '실행 중인 객체의 실제 타입'에 따라 다른 동작을 할 수 있게 하는 것이다.<br>
<br>

<b>[예시 - C++]<br></b>

```c++
#include <iostream>
using namespace std;

class Base {
  public:
    virtual void show() {
      cout << "Base class show function called" << endl;
    }
};

class Derived : public Base {
  public:
    void show() {
      cout << "Derived class show function called" << endl;
    }
};

int main() {
  Base* baseptr;
  Derived derivedObj;

  baseptr = &derivedObj;

  // 런 타임 다형성
  baseptr->show();

  return 0;
}
```
<br>

<b>[예시 - C#]<br></b>

```c#
using System;

public class Base {
  public virtual void Show() {
      Console.WriteLine("Base class Show function called");
  }
}

public class Derived : Base {
  public override void Show() {
      Console.WriteLine("Derived class Show function called");
  }
}

class Program {
  static void Main() {
      Base baseObj = new Base();
      baseObj.Show(); // 기반 클래스의 Show 호출

      baseObj = new Derived();
      baseObj.Show(); // 런 타임 다형성으로 파생 클래스의 Show 호출
  }
}
```
<br>
<br>
<br>

## 다형성의 장/단점

### 장점

<b>유연성과 확장성</b>
<br>: 다형성을 사용하면, 새로운 클래스 형식을 추가하거나 기존 코드를 수정하지 않고도, 새로운 기능을 쉽게 추가할 수 있다.<br>
<br>

<b>코드 재사용</b>
<br>: 공통의 인터페이스를 사용하여 다양한 구현을 제공함으로써, 코드의 재사용성을 크게 높일 수 있다.<br>
<br>

<b>인터페이스 분리</b>
<br>: 다형성을 통해 `클라이언트 코드` 는 `구체적인 클래스 타입` 보다는 `인터페이스` 나 `추상 클래스` 에 의존할 수 있어, 결합도를 낮출 수 있다.<br>
<br>


### 단점

<b>복잡성 증가</b>
<br>: 다형성을 지나치게 사용하면 프로그램의 구조가 복잡해질 수 있다.<br>
'다양한 클래스' 들이 '같은 인터페이스' 를 공유하므로, 프로그램의 흐름을 이해하고 디버깅 하는 데에 어려움이 커질 수 있다.<br>
<br>

<b>성능 저하</b>
<br>: `런 타임 다형성` 은 `가상 함수 호출` 을 사용하는데, `가상 함수 호출` 은 `직접 함수 호출` 보다 비용이 더 많이 들 수 있다.<br>
<br>

<b>오용 가능성</b>
<br>: 다형성을 잘못 사용하면 코드를 더욱 혼란스럽게 만들고, 유지보수에 어려움을 가져다줄 수 있다.<br>
<br>

<b>디자인의 제약</b>
<br>: 다형성을 사용하려면 <b>클래스 계층을 신중하게 설계</b>해야 한다.<br>
잘못 설계된 클래스 계층은 프로그램의 유연성을 오히려 저해시키고, 확장성을 제한시킬 수 있다.<br>

<br><br><br>
