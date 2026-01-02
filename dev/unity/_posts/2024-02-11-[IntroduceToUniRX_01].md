---
layout: single
title: "UniRX 입문 (1) - soo:bak"
date: "2024-02-12 03:18:00 +0900"
description: "UniRx 입문 시리즈 첫 번째 글입니다. 데이터 스트림, IObservable, IObserver, Subscribe의 개념을 설명합니다."
tags:
  - Unity
  - UniRx
  - 반응형 프로그래밍
  - Reactive Extensions
  - C#
  - 게임 개발
keywords: "UniRx 입문, IObservable, IObserver, Subscribe, 데이터 스트림, 반응형 프로그래밍, Unity"
---
<br>

`UniRX` 의 입문과 사용에 있어서 보다 체계적으로 정리를 해보고자 글을 작성합니다.<br>
<br>

## UniRx 입문
먼저, 무엇인가 처음 접할 때 학습의 효율성을 가장 높여주는 것 중 하나는 '해당 학습으로 인하여 얻을 수 있는 것' 을 보다 명확히 인지하는 것이라고 생각합니다.<br>
<br>
이 부분에 있어서, 지난 2017년 Unite 17 에서의 [박민근 님의 발표 영상](https://www.youtube.com/watch?v=NN1_41TE1N0) 이 가장 좋은 자료 중 하나라고 생각합니다.<br>
<br>
본격적인 `UniRX` 학습 시작 이전, 시청해보시길 추천드리는 멋진 발표입니다.<br>
<br>
`UniRX` 의 장점과 사용 의미에 대해서 보다 명확히 인지할 수 있습니다.<br>
<br>
<br>
<br>
또한, `UniRX` 는 `관찰자 패턴(Observer pattern)` 이라는 디자인 패턴을 따릅니다.<br>
<br>
따라서, `UniRX` 학습 이전 해당 디자인 패턴에 대한 기초적인 지식을 가볍게나마 학습하시는 것을 권장드립니다.<br>
<br>
<br>
[관찰자 패턴(Observer Pattern) 기초 - soo:bak](https://soo-bak.github.io/dev/design-&-architecture/design-pattern/ObserverPattern/)<br>
<br>
<br>
<br>
<br>
<br>
또한, `UniRX` 가 등장한 2017년도는 지금 이 글을 작성하는 시점(2024년)으로부터 약 7년이라는 꽤 많은 시간이 흐른 시점이라는 것도 알아두시면 좋을 것 같습니다.<br>
<br>
특히, 변화가 빠른 소프트웨어 분야에서 7년이라는 기간은 더욱 짧지 않은 기간입니다.<br>
<br>
그 동안 많은 것들이 변해왔고, `UniRX` 가 등장했던 시기의 상황과 지금의 상황 또한 많이 달라졌다는 것을 인지하시는 것이, 개인적으로 생각하는 올바른 프로그래머의 자세라고 생각합니다.<br>
<br>
<br>
해당 부분과 관련하여서는, 다음 두 개 블로그를 참고해보시는 것을 추천드립니다.<br>
<br>
각각 원문과 번역 글인데, 번역해주신 역자분의 블로그에도 `UniRX` 관련 글들도 도움이 되는 내용이 많으니, 참고해보시면 도움이 되실 것 같습니다.<br>
<br>
- [2022年現在におけるUniRxの使いみち (원문)](https://qiita.com/toRisouP/items/af7d32846ab99f493d92)
- [2022년 현재 UniRx의 용도 (번역)](https://tech.lonpeach.com/2022/10/29/2022-unirx/)
<br>
<br>
<br>
<br>
<br>
<br>

<i>"하나의 아이스크림만 먹어봤다면, 평생 다른 아이스크림의 맛은 모를 것이다. 만약, 여러가지 아이스크림을 맛보았다면 '선택' 이라는 것을 할 수 있다."</i><br>
<br>
얼마전, 개인적으로 좋아하는 개발자분께서 저에게 해주신 말씀입니다.<br>
<br>
그 당시 꽤나 인상깊었던 조언이어서, 간단히 소개드리면서 본격적인 `UniRX` 학습을 시작해보고자 합니다.<br>
<br>
<br>
<br>
<br>

## UniRX 와 전통적인 관찰자 패턴
[관찰자 패턴(Observer Pattern) 기초 - soo:bak](https://soo-bak.github.io/dev/design-&-architecture/design-pattern/ObserverPattern/) 에서 다루었던 것 처럼, <br>
<br>
관찰자 패턴의 기본 구성 요소는 `주체(Subject)` 와 `관찰자(Observer)` 입니다.<br>
<br>
<br>
간단히 요약해보면, <br>
<br>
<br>

<b>주체(Subject)</b>
<br>: `관찰 대상 객체`입니다.<br>
<br>
상태 변화가 발생할 때, `관찰자` 들에게 알림을 보냅니다.<br>
<br>
<br>

<b>관찰자(Observer)</b>
<br>:`주체` 의 상태 변화를 관찰하는 객체입니다.<br>
<br>
`주체` 로 부터 알림을 받으면 적절한 반응을 합니다.<br>
<br>
<br>

`UniRX` 에는 위의 `주체` 와 `관찰자` 역할을 하는 `IObservable<T>` 와 `IObserver<T>` 라는 인터페이스가 존재합니다.<br>
<br>
<br>
<b>`IObservable<T>` (주체 역할)</b>
<br>: 이 인터페이스는 `데이터 스트림` 또는 `이벤트` 의 <b>근원</b> 역할을 합니다.<br>
<br>
즉, `관찰자` 객체들이 자신을 `구독` 하게 하며, 상태 변화가 발생할 때 구독자들에게 변화에 대해서 알립니다.<br>
<br>
> '데이터 스트림', '구독' 이라는 용어에 대해서는 이후에 더욱 명확하게 다룹니다.<br>
해당 용어는 '반응형 프로그래밍' 과 관련이 있습니다. <br>
우선 지금은 '전통적인 관찰자 패턴' 의 관점에 조금 더 초점을 맞추어서, IObservable<T> 의 '주체' 역할에 초점을 맞추는 것을 권장드립니다.<br>

<br>
<br>
<b>`IObserver<T>` (관찰자 역할)</b>
<br>: 이 인터페이스는, 위의 `IObservable<T>` 로부터 발생하는 알림을 관찰하고, 수신하는 역할을 합니다.<br>
<br>
즉, `IObservable<T>` 의 상태 변화를 감지하고, 이에 대응합니다.<br>
<br>
<br>
<br>
<br>

## `IObservable<T>` (주체 역할)
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
<br>

## 구독(Subscribe)
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

이 때, <b>주체</b>역할을 하는 `IObservable<T>` 와, <b>관찰자</b> 역할을 하는 `IObserver<T>` 사이의 연결고리가 바로,<br>
<br>
`Subscribe(구독)` 입니다.<br>
<br>
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
구독을 통해 `IObservable<T>` 는 `IObserver<T>` 에게 `데이터 스트림` 의 변화를 알릴 수 있게 된다.<br>
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
