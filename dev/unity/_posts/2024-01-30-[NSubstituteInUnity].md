---
layout: single
title: "Unity 에서의 NSubstitute 사용 - soo:bak"
date: "2024-01-30 01:03:00 +0900"
description: "Unity 프로젝트에서 NSubstitute를 활용한 단위 테스트 작성 방법을 다양한 예제와 함께 상세히 설명합니다."
tags:
  - Unity
  - NSubstitute
  - 단위 테스트
  - TDD
  - C#
  - 게임 개발
keywords: "Unity NSubstitute, 단위 테스트, TDD, 모킹, 게임 개발, C#, 의존성 주입"
---
<br>
<br>
<b>관련 글  : </b> [NSubstitute : .Net Mocking Framework - soo:bak](https://soo-bak.github.io/dev/methodology/test-driven-development/NSubstitute_Basic/#page-title)
<br><br><br>

## `NSubstitute` 를 유니티에서 사용하기
`NSubstitute` 는 유니티 프로젝트에서 단위 테스트를 수행하고 종속성을 격리하는 좋은 도구로 활용될 수 있다.<br>
<br><br>

### 예제 시나리오 가정
만약, 유니티 게임 프로젝트에서 플레이어(Player) 와 적(Enemy) 사이의 상호 작용을 테스트 하려고 하고,<br>
<br>
이를 위해 `IEnemy` 인터페이스와 `Player` 클래스가 다음과 같이 정의되어 있다고 가정하자 :<br>
<br>

```c#
using System;

// IEnemy 인터페이스 정의
public interface IEnemy {
  int Health { get; set; }
  int TakeDamage(int amount);
  void AttackPlayer();
  event EventHandler Died;
}

// Player 클래스
public class Player {
  private IEnemy enemy;

  public Player(IEnemy enemy) {
    this.enemy = enemy;
  }

  public int AttackEnemy() {
    return enemy.TakeDamage(10);
  }

  public int AttackEnemy(int damage) {
    return enemy.TakeDamage(damage);
  }

  public int GetEnemyHealth() {
    return enemy.Health;
  }
}
```
<br><br>

## `NSubstitute` 를 사용한 단위 테스트
<br>
<b>1. 가짜 객체 생성</b><br>
<br>
먼저, `IEnemy` 인터페이스의 가짜 객체를 생성한다.<br>
<br>
이 객체는 테스트 중에 적(Enemy) 역할을 대신할 것이다.<br>
<br>

```c#
IEnemy fakeEnemy = Substitute.For<IEnemy>();
```
<br><br>
<b>2. 의존성 주입</b><br>
<br>
가짜 객체를 생성한 후, 이를 이용해 `Player` 클래스의 인스턴스를 생성한다.<br>
<br>
이렇게 하면 `Player` 클래스가 실제 적(Enemy)이 아닌 가짜 객체와 상호 작용 할 수 있게 된다.<br>
<br>

```c#
Player player = new Player(fakeEnemy);
```
<br><br>
<b>3. 메서드 호출 검증</b><br>
<br>
이제 `Player` 클래스의 `AttackEnemy()` 메서드를 호출하고, 특정 동작이 예상대로 수행되었는지 검증한다.<br>
<br>
예를 들어, `AttackEnemy()` 메서드가 내부에서 `enemy.TakeDamage(10)` 을 호출하는지를 확인하려면 다음과 같이 검증할 수 있다 : <br>
<br>

```c#
// Act : 플레이어가 적을 공격함
player.AttackEnemy();

// Assert : 적(가짜 객체)이 TakeDamage 메서드를 10의 인수로 호출했는지 검증
fakeEnemy.Received().TakeDamage(10);
```
<br><br>
<b>4. 동작 설정</b><br>
<br>
가짜 객체의 메서드 호출 동작을 설정하려면, `When` 과 `Do` 메서드를 사용한다.<br>
<br>
예를 들어, 적이 `AttackPlayer()` 메서드를 호출했을 때 어떤 동작을 수행하도록 설정하려면 다음과 같이 한다 :
<br>
```c#
fakeEnemy.When(e => e.AttackPlayer()).Do(e => { /* 동작 설정 */ });
```
<br><br>


### 완성된 테스트 코드
<br>
위에서 설명한 내용을 종합하여 완성된 테스트 코드는 다음과 같다 : <br>
<br>

```c#
using NSubstitute;
using NUnit.Framework;

[TestFixture]
public class PlayerTests {

  [Test]
  public void Player_AttackEnemy_DamagesEnemy() {

    // Arrange
    IEnemy fakeEnemy = Substitute.For<IEnemy>();
    Player player = new Player(fakeEnemy);

    // Act
    player.AttackEnemy();

    // Assert
    fakeEnemy.Received(1).TakeDamage(10);

  }

}
```
<br>
이 테스트는 `Player` 가 `AttackEnemy()` 메서드를 호출할 때, `IEnemy` 의 `TakeDamage(10)` 메서드가 한 번 호출되는지 검증한다.<br>
<br><br><br>

## 결론
유니티 프로젝트에서 `NSubstitute` 를 사용하여 단위 테스트를 작성하는 것은 코드의 견고성을 높이고, 버그를 줄이는 데 큰 도움이 된다.<br>
<br>
단위 테스트를 통해 유니티 프로젝트를 더 품질 높게 개발할 수 있도록 `NSubstitute` 를 적극적으로 활용해보자.

<br><br><br><br><br><br>

## 다양한 예시
<br>

### 예시 1. 메서드 호출 검증
<br>
<b>`TakeDamage()` 메서드 호출 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_DamagesEnemy() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 공격함
  player.AttackEnemy();

  // Assert : 적(가짜 객체)이 TakeDamage 메서드를 10의 인수로 호출했는지 검증
  fakeEnemy.Received().TakeDamage(10);

}
```
<br><br><br>

### 예시 2. 메서드 호출 순서 검증
<br>
<b>`AttackPlayer()` 와 `TakeDamage()` 메서드 호출 순서 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_CorrectMethodCallOrder() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 공격함
  player.AttackEnemy();

  // Assert : 메서드 호출 순서 검증
  Received.InOrder(() => {
    fakeEnemy.AttackPlayer();
    fakeEnemy.TakeDamage(10);
  });
}
```
<br><br><br>

### 예시 3. 예외 던지기
<br>
<b>`TakeDamage()` 메서드가 예외를 던지는 경우를 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ThrowsException() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(Arg.Any<int>())
    .Returns(x => { throw new Exception("Damage failed!"); });
  Player player = new Player(fakeEnemy);

  // Act & Assert : 특정 동작이 예외를 던지는지 검증
  Assert.Throws<Exception>(() => player.AttackEnemy());
}
```
<br><br><br>

### 예시 4. 메서드 반환값 설정
<br>
<b>`TakeDamage()` 메서드의 반환값을 설정하고 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ReturnsValue() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(Arg.Any<int>()).Returns(5);
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 공격함
  int damageDealt = player.AttackEnemy();

  // Assert : 반환값 검증
  Assert.AreEqual(5, damageDealt);
}
```
<br><br><br>

### 예시 5. 메서드가 특정 횟수 호출되는지 검증
<br>
<b>`TakeDamage()` 메서드가 두 번 호출되는지 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_CallsMethodMultipleTimes() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 두 번 적을 공격함
  player.AttackEnemy();
  player.AttackEnemy();

  // Assert : 메서드 호출 횟수 검증
  fakeEnemy.Received(2).TakeDamage(10);
}
```
<br><br><br>

### 예시 6. 메서드가 특정 조건에 따라 다르게 동작하는지 검증
<br>
<b> `TakeDamage()` 메서드가 특정 인수에 따라 다른 값을 반환하는지 검증</b>
<br>

```c#
[Test]
public void Player_TakeDamage_ReturnsDifferentValuesBasedOnInput() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(5).Returns(10);  // 5 입력 시 반환값 10 설정
  fakeEnemy.TakeDamage(10).Returns(20); // 10 입력 시 반환값 20 설정
  Player player = new Player(fakeEnemy);

  // Act & Assert
  int damage1 = player.AttackEnemy(5);
  int damage2 = player.AttackEnemy(10);

  // 다른 입력에 따른 반환값 검증
  Assert.AreEqual(10, damage1);
  Assert.AreEqual(20, damage2);
}
```
<br><br><br>

### 예시 7. 메서드 호출 시 인수 검증
<br>
<b> `TakeDamage()` 메서드가 특정한 인수 값으로 호출되었는지 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_CallsMethodWithSpecificArgument() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 공격함
  player.AttackEnemy();

  // Assert : 메서드 호출 시 특정 인자값 검증
  fakeEnemy.Received().TakeDamage(Arg.Is<int>(x => x == 10));
}
```
<br><br><br>

### 예시 8. 가짜 객체의 프로퍼티 설정
<br>
<b> 적(Enemy)의 체력을 설정하고 반환하는 상황을 검증</b>
<br>

```c#
[Test]
public void Player_GetEnemyHealth_ReturnsEnemyHealth() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.Health.Returns(100); // 체력 프로퍼티 설정
  Player player = new Player(fakeEnemy);

  // Act : 적의 체력 조회
  int enemyHealth = player.GetEnemyHealth();

  // Assert : 프로퍼티 반환 값 검증
  Assert.AreEqual(100, enemyHealth);
}
```
<br><br><br>

### 예시 9. 가짜 객체의 이벤트 시뮬레이션
<br>
<b> 가짜 객체에서 이벤트를 발생시키고, 특정 이벤트 핸들러가 호출되는지 검증</b>
<br>

```c#
[Test]
public void Enemy_Died_RaisesEvent() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  bool eventRaised = false;

  // 이벤트 핸들러 등록
  fakeEnemy.Died += (sender, args) => eventRaised = true;

  // Act : 이벤트 발생 시뮬레이션
  fakeEnemy.Died += Raise.Event();

  // Assert : 이벤트가 발생하고 핸들러가 호출되는지 검증
  Assert.IsTrue(eventRaised);
}
```
<br><br><br>

### 예시 10. 가짜 객체의 메서드 호출 동작 설정
<br>
<b> 가짜 객체의 메서드 호출 시 특정 동작을 수행하도록 설정하는 예시,<br>
예를 들어, 메서드가 호출될 때 값을 변경하는 동작을 설정하여 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ModifiesValue() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  int health = 100;

  // 메서드 호출 시 동작 설정
  fakeEnemy.TakeDamage(Arg.Any<int>()).Returns(x => {
    int damage = x.ArgAt<int>(0);
    health -= damage;
    return damage;
  });

  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 공격함
  int damageDealt = player.AttackEnemy();

  // Assert : 메서드 호출 후 값이 변경되었는지 검증
  Assert.AreEqual(90, health); // 100 - 10
  Assert.AreEqual(10, damageDealt);
}
```
<br><br><br>

### 예시 11. 메서드가 특정 조건에 따라 예외 던지기
<br>
<b> 메서드 호출 시 특정 조건을 만족하지 않으면 예외를 던지도록 설정 후 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ThrowsExceptionForNegativeDamage() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(Arg.Is<int>(x => x < 0))
    .Returns(x => { throw new ArgumentException("Negative damage is not allowed!"); });
  Player player = new Player(fakeEnemy);

  // Act & Assert : 특정 조건에 따라 예외를 던지는지 검증
  Assert.Throws<ArgumentException>(() => player.AttackEnemy(-5));
}
```
<br><br><br>

### 예시 12. 메서드가 호출되지 않았는지 검증
<br>
<b> 특정 조건에서 메서드가 호출되지 않았음을 검증</b>
<br>

```c#
[Test]
public void Player_DoesNotAttack_WhenNotCalled() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 아무 동작도 하지 않음

  // Assert : TakeDamage가 호출되지 않았는지 검증
  fakeEnemy.DidNotReceive().TakeDamage(Arg.Any<int>());
}
```
<br><br><br>

### 예시 13. 가짜 객체의 메서드 반환값 동적 설정 검증
<br>
<b> 가짜 객체의 메서드 호출 시 동적으로 반환값을 설정 후 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ReturnsDynamicValue() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(Arg.Any<int>()).Returns(x => x.ArgAt<int>(0) * 2); // 인자에 따라 반환값 동적 설정
  Player player = new Player(fakeEnemy);

  // Act : 메서드 호출 시 동적으로 반환값이 설정되는지 검증
  int damage1 = player.AttackEnemy(5);  // 5 * 2 = 10
  int damage2 = player.AttackEnemy(8);  // 8 * 2 = 16

  // Assert
  Assert.AreEqual(10, damage1);
  Assert.AreEqual(16, damage2);
}
```
<br><br><br>

### 예시 14. 메서드 호출 횟수가 최소 N회 이상인지 검증
<br>
<b> 메서드가 특정 횟수 이상 호출되었는지 검증</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_CallsMethodAtLeastTwice() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  Player player = new Player(fakeEnemy);

  // Act : 플레이어가 적을 여러 번 공격함
  player.AttackEnemy();
  player.AttackEnemy();
  player.AttackEnemy();

  // Assert : 메서드가 최소 2회 이상 호출되었는지 검증
  fakeEnemy.ReceivedWithAnyArgs(Quantity.AtLeastOne()).TakeDamage(default);
  // 또는 정확한 횟수 검증
  fakeEnemy.Received(3).TakeDamage(10);
}
```
<br><br><br>

### 예시 15. 순차적 반환값 설정
<br>
<b> 메서드가 호출될 때마다 다른 값을 순차적으로 반환하도록 설정</b>
<br>

```c#
[Test]
public void Player_AttackEnemy_ReturnsSequentialValues() {

  // Arrange : 가짜 적(Enemy) 객체 생성
  IEnemy fakeEnemy = Substitute.For<IEnemy>();
  fakeEnemy.TakeDamage(Arg.Any<int>()).Returns(10, 20, 30); // 순차적 반환값 설정
  Player player = new Player(fakeEnemy);

  // Act & Assert : 호출할 때마다 다른 값 반환
  Assert.AreEqual(10, player.AttackEnemy());
  Assert.AreEqual(20, player.AttackEnemy());
  Assert.AreEqual(30, player.AttackEnemy());
}
```
