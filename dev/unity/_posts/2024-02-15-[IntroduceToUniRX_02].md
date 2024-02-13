---
layout: single
title: "UniRX 입문 (2) - soo:bak"
date: "2024-02-15 03:39:00 +0900"
---
<br>

`UniRX` 의 입문과 사용에 있어서 보다 체계적으로 정리를 해보고자 글을 작성합니다.<br>
<br>

[이전 글 : UniRX 입문 (1) - soo:bak]()<br>
<br>
<br>
<br>

## `IObserver<T>` (관찰자 역할)


## `IDisposable`

## `IDisposable Subscribe(IObserver<T> observer)`


`주체` 역할을 하는 `IObservable<T>` 는 다음과 같은 원형을 가지고 있습니다.<br>
<br>

```c#
public interface IObservable<T> {
  IDisposable Subscribe(IObserver<T> observer);
}
```
<br>
한 번 살펴보면, <br>
<br>
`IDisposable` 타입을 반환하며, `IObserver<T>` 을 매개변수로 하는 `Subscribe` 메서드 하나만이 선언되어 있는 간단한 인터페이스 입니다.<br>
<br>
`IDisposalbe` 타입은 잠시 뒤로 미뤄두고,<br>
<br>
과연 이 `Subscribe` 메서드의 역할은 무엇일까요?<br>
<br>
<br>

### 구독(Subscribe)
`Subscribe` 메서드는 `IObservable<T>` 인터페이스에 선언되어 있다는 점을 다시 되새겨 봅시다.<br>
<br>
또한, `IObservable<T>` 인터페이스는 `관찰자 패턴` 에서 `주체` 역할을 하는 객체에 대한 인터페이스 라는 점도 같이 되새겨 봅시다.<br>
<br>
<br>

<b>전통적인 관찰자 패턴</b>에서 `주체(Subject)` 객체는 상태 변경을 `관찰자(Observer)` 에게 알립니다.<br>
<br>
또한, 각 `관찰자` 는 `주체` 의 상태 변경을 `감지` 하고, 이에 `반응` 합니다.<br>
<br>
<br>

`RX` 에서 이러한 개념들은 `데이터 스트림` 처리의 맥락으로 확장됩니다. <br>
<br>
이 때, `데이터 스트림` 이라는 용어가 어려운 것 같지만, 용어가 낯설 뿐, 쉬운 내용입니다.<br>
<br>
<br>

> 데이터 스트림(Data Stream)<br>
<br>
`데이터 스트림` 은 <b>'시간에 따라 연속적으로 생성되고 처리되는 데이터의 순차적인 흐름'</b> 입니다.<br>
<br>
즉, 다음과 같은 특징을 가집니다. <br>
<br>
<br>
<b>연속성</b><br>
<br>: 데이터 스트림은 끊임없이 '흐르는' 데이터로 구성됩니다.<br>
<br>
즉, 데이터가 시간에 따라서 계속해서 제공됩니다.<br>
<br>
<br>
<b>순차적 처리</b><br>
<br>: 스트림의 데이터는 일반적으로 '도착한 순서대로' 처리됩니다.<br>
<br>
즉, 각각의 데이터 값들은 스트림을 따라서 한 번에 하나씩 이동하며, 각 값들은 다음 단계로 전달되기 전에 처리됩니다.<br>
<br>
<br>
<b>무한성</b><br>
<br>: 데이터 스트림은 이론적으로 <b>끝이 없을 수</b>있습니다.<br>
<br>
예를 들어, 소셜 미디어 피드나 센서 데이터 등은 애플리케이션이 실행되는 동안 계속해서 데이터를 생성할 수 있습니다.<br>
<br>
<br>
<b>동적</b><br>
<br>: 데이터 스트림은 시간의 흐름에 따라서 변화할 수 있는 동적인 데이터를 포함합니다.<br>
<br>
즉, 데이터의 속성, 속도 또는 구조가 시간이 지남에 따라 변할 수 있습니다.<br>

<br>
<br>
다시 `Subscribe` 메서드에 대한 설명으로 돌아와서,<br>
<br>
<i>"</i>`RX` <i>에서 전통적인 관찰자 패턴은 </i>`데이터 스트림` <i>의 처리의 맥락으로 확장된다."</i> 라는 말을 다시 살펴봅시다.<br>
<br>
`RX` 에서 `IObservable<T>` 는 <b>주체</b>의 역할을 하며, `IObserver<T>` 는 <b>관찰자</b>의 역할을 합니다.<br>
<br>
그러나 `RX` 에서는, 전통적인 관찰자 패턴에서 처럼 단순히 '상태 변경을 알리는 것' 을 넘어서,<br>
<br>
<b>시간에 따라 변화하는</b> `데이터 스트림` <b>을 다룹니다.</b><br>
<br>
<br>

이 때, <b>주체</b>역할을 하는 `IObservable<T>` 와, <b>관찰자</b> 역할을 하는 `IObserver<T>` 사이의 연결고리가 바로 `Subscribe(구독)` 입니다.<br>
<br>
<br>

## 정리 & 예습
이번 글에서 주로 다루었던, `데이터 스트림`, `IObservable<T>`, `Subscribe(구독)의 간단한 정의` 에 대해 정리합니다.<br>
<br>
그리고, 다음 글에서 더 자세하게 다룰 `IObserver<T>` 와 `Subscribe` 메서드의 반환 타입인 `IDisposable` 과 관련된 '데이터 스트림의 리소스 관리' 에 대해서도 간단히 예습해봅니다.<br>
<br>
<br>

### 데이터 스트림
데이터 스트림은 '시간에 따라 연속적으로 생성되고 처리되는 데이터의 순차적 흐름' 을 나타낸다.<br>
<br>
`UniRX` 에서 `IObservable<T>` 는 데이터 스트림의 '근원' 이며,<br>
<br>
데이터 항목, 오류 또는 완료 신호를 시간에 따라 방출할 수 있는 객체이다.<br>
<br>
<br>
<br>

### `IObservable<T>` (주체 역할)
`IObservable<T>` 인터페이스는 전통적인 관찰자 패턴에서 주체(Subject)의 역할을 확장한 것이다.<br>
<br>
주체는 관찰자에게 상태 변경을 알리는 역할을 하며, `UniRX` 에서는 `IObservable<T>` 가 이 역할을 수행한다.<br>
<br>
하지만, `UniRX` 에서는 '단순한 상태 변경' 을 넘어서, '시간에 따라 변화하는 데이터 스트림' 을 관찰자에게 전달한다.<br>
<br>
<br>
<br>

### `IObserver<T>` (관찰자 역할)
`IObserver<T>` 인터페이스는 관찰자의 역할을 정의한다.<br>
<br>
이 인터페이스는 `OnNext`, `OnError`, `OnCompleted` 의 세 메서드를 통해 `데이터 스트림` 의 다양한 상태를 처리한다.<br>
<br>
`OnNext` 는 새 데이터 항목이 방출될 때 호출되며, `OnError` 는 오류가 발생했을 때, `OnCompleted` 는 `데이터 스트림` 이 완료되었을 때 호출된다.<br>
<br>
<br>
<br>

### 구독(Subscribe)
구독은 `IObserver<T>` 가 `IObservable<T>` 에 자신의 관찰을 연결하는 과정이다.<br>
<br>
이 과정은 `IObservable<T>` 의 `Subscribe` 메서드를 호출함으로써 수행된다.<br>
<br>
구독을 통해 `IObservable<T>` 는 `IObservable<T>` 에게 `데이터 스트림` 의 변화를 알릴 수 있게 된다.<br>
<br>
`Subscribe` 메서드는 `IDisposable` 인터페이스를 구현하는 객체를 반환하여, 구독자가 필요할 때 언제든지 구독을 해제할 수 있는 방법을 제공한다.<br>
<br>
<br>
<br>

### 구독의 중요성
구독 메커니즘은 `IObservable<T>` 와 `IObserver<T>` 사이의 동적인 연결을 가능하게 한다.<br>
<br>
이는 `데이터 스트림` 이 동적이고, 구독자가 실행 시간(런 타임)에 따라 변할 수 있음을 반영한다.<br>
<br>
`구독` 을 통해 `구독자` 는 관심 있는 `데이터 스트림` 에 대한 갱신을 확인할 수 있으며, `데이터 스트림` 의 생명주기 관리와 리소스 관리에 중요한 역할을 한다.<br>
<br>
<br>
