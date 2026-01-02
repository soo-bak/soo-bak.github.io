---
layout: single
title: "관찰자 패턴(Observer Pattern) 기초 - soo:bak"
date: "2024-02-04 20:46:00 +0900"
description: "관찰자 패턴의 개념, 구성 요소, 작동 원리, 장단점을 C# 예제와 함께 설명합니다. 발행-구독 모델의 기초입니다."
tags:
  - 디자인 패턴
  - 관찰자 패턴
  - Observer Pattern
  - C#
  - 이벤트
  - 소프트웨어 설계
keywords: "관찰자 패턴, Observer Pattern, 발행-구독, Publish-Subscribe, MVC, 디자인 패턴, C# 이벤트"
---
<br>

## 관찰자 패턴(Observer Pattern)
객체 지향 디자인 패턴 중 하나,<br>
<br>
한 객체의 상태 변화를 관찰하고 있는 다른 객체들, 즉, '관찰자' 들에게 상태 변화를 자동으로 통지하는 방식이다.<br>
<br>
주로 분산 이벤트 핸들링 시스템에서, 이벤트가 발생했을 때 여러 객체에게 알려야 할 경우에 사용한다.<br>
<br>
'발행-구독 모델(Publish-Subscribe Model)' 이라고도 불리며,<br>
<br>
MVC(Model-View-Controller) 아키텍쳐 패턴의 핵심 구성요소 중 하나이다.
<br><br><br>

## 구성 요소
관찰자 패턴은 주로 다음의 네 가지 구성 요소로 이루어 진다.<br>
<br>
- 주체(Subject)
<br>: 관찰 대상 객체로, 관찰자들을 등록, 제거, 통지하는 메서드를 제공한다.<br>
주체는 관찰자 목록을 유지/관리하며, 상태 변화가 있을 때 등록된 모든 관찰자들에게 통지(`notify`)한다.<br>
<br>
- 관찰자(Observer)
<br>: 주체의 상태 변화를 관찰하고 있는 객체들로, 주체로부터 상태 변화 통지를 받을 때 마다 반응하는 메서드(`update`)를 정의한다.<br>
관찰자는 하나 이상의 주체를 관찰할 수 있다.<br>
<br>
- 구체적인 주체(Concrete Subject)
<br>: `Subject` 인터페이스를 구현하거나, `Subject` 클래스를 확장하여, 실제 관찰 대상의 역할을 하는 클래스.<br>
이 클래스에서는 상태 변화를 관리하고, 상태 변화가 있을 때 모든 관찰자에게 통지한다.<br>
<br>
- 구체적인 관찰자(Concrete Observer)
<br>: `Observer` 인터페이스를 구현하거나, `Observer` 클래스를 확장하여, 실제로 상태 변화에 반응하는 클래스.<br>
구체적인 관찰자는 주체의 상태 변화를 받고, 그에 따른 적절한 행동을 취한다.<br>
<br><br><br>

## 작동 원리
`Subject` 객체의 상태가 변화하면, 등록된 모든 `Observer` 들에게 상태 변화를 통지한다.<br>
<br>
`Observer` 는 `Subject` 로부터 통지를 받고, 필요한 조치를 취한다.<br>
<br>

## 장점
- 낮은 결합도
<br>: 주체와 관찰자 사이의 결합도가 낮아, 시스템의 유연성과 확장성이 향상된다.<br>
<br>
- 재사용성 향상
<br>: 주체나 관찰자를 변경하지 않고도, 새로운 관찰자를 쉽게 추가할 수 있어 코드의 재사용성이 향상된다.<br>
<br>
- 실시간 갱신
<br>: 주체의 상태 변화를 실시간으로 관찰자들에게 통지함으로써, <b>동기화된 상태</b>를 유지할 수 있다.<br>
<br><br><br>

## 단점
- 메모리 누수
<br>: 주체와 관찰자 사이에 순환 참조가 발생할 경우, 메모리 누수가 발생할 수 있다.<br>
<br>
- 성능 이슈
<br>: 많은 수의 관찰자가 등록되어 있을 경우, 상태 변화를 통지하는 과정에서 성능 저하가 발생할 수 있다.<br>
<br><br><br>

## 구현 예시
<br>

### 플레이어의 생명력이 변경될 때마다 관련 UI 컴포넌트에 알리는 예시
<br>

```c#
using System;

public class HealthManager {
  public event Action<int> OnHealthChanged;
  private int health;

  public int Health {
    get { return health; }
    set {
      health = value;
      OnHealthChanged?.Invoke(health);
    }
  }

  public void TakeDamage(int damage) {
    Health = Math.Max(Health - damage, 0);
  }
}

public class HealthDisplay {
  public HealthDisplay(HealthManager healthManager) {
    healthManager.OnHealthChanged += UpdateHealthDisplay;
  }

  private void UpdateHealthDisplay(int health) {
    Console.WriteLine($"Health: {health}");
  }
}
```
<br>

### 특정 게임 이벤트가 발생할 때 여러 시스템에 알리는 예시
<br>

```c#
using System;

public class GameManager {
  public event Action<string> OnGameEvent;

  public void TriggerEvent(string eventName) {
    OnGameEvent?.Invoke(eventName);
  }
}

public class AchievementSystem {
  public AchievementSystem(GameManager gameManager) {
    gameManager.OnGameEvent += CheckForAchievement;
  }

  private void CheckForAchievement(string eventName) {
    if (eventName == "LevelCleared")
      Console.WriteLine("Achievement Unlocked: Level Cleared!");
  }
}
```
<br>

### 사용자 입력 반응
개념적 설명을 위한 예시 코드
<br>

```c#
using System;

public class InputManager {
  public event Action OnJumpPressed;

  public void CheckForJump() {
    // 여기서는 입력 검사를 시뮬레이션, 실제 게임에서는 입력 시스템을 통해 이벤트를 Trigger 해야 함
    if (Console.ReadKey().Key == ConsoleKey.Spacebar)
      OnJumpPressed?.Invoke();
  }
}

public class PlayerController {
  public PlayerController(InputManager inputManager) {
    inputManager.OnJumpPressed += PerformJump;
  }

  private void PerformJump() {
    Console.WriteLine("Player Jump!");
  }
}
```
<br>

### 데이터 스트림 필터링
<br>

```c#
using System;

public class NetworkManager {
  public event Action<string> OnMessageReceived;

  public void ReceiveMessage(string message) {
    OnMessageReceived?.Invoke(message);
  }
}

public class MessageFilter {
  public MessageFilter(NetworkManager networkManager) {
    networkManager.OnMessageReceived += CheckForErrorMessage;
  }

  private void CheckForErrorMessage(string message) {
    if (message.Contains("Error"))
      Console.WriteLine($"Error Message Received: {message}");
  }
}
```
<br>
<br>
<br>
