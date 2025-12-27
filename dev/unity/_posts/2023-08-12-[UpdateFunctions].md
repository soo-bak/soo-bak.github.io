---
layout: single
title: "Unity 의 Update, FixedUpdate 그리고 LateUpdate - soo:bak"
date: "2023-08-12 11:50:00 +0900"
description: "Unity의 Update, FixedUpdate, LateUpdate 메서드의 호출 시점, 용도, 차이점을 상세히 설명합니다."
tags:
  - Unity
  - Update
  - FixedUpdate
  - LateUpdate
  - 게임 개발
  - MonoBehaviour
keywords: "Unity Update, FixedUpdate, LateUpdate, Time.deltaTime, 물리 연산, Unity 게임 개발, MonoBehaviour"
---
<br>

게임 개발에 있어서 로직의 흐름을 제어하는 것은 굉장히 중요한 일이다. <br>
<br>
특히 `Unity` 엔진에서는 "Order of Execution for Event Functions" 라는 중요한 개념이 있는데,<br>
<br>
이는 작성된 스크립트의 메서드들이 언제, 어떤 순서로 호출될 것인가를 결정한다.<br>
<br>
그 중에서도 `Update`, `FixedUpdate` 그리고 `LateUpdate` 실행 시점에서 게임 로직의 핵심을 담당하게 된다.<br>
<br>
따라서, 이 세 메서드들의 역할과 호출 시점, 그리고 이들이 게임 내에서 어떻게 작용하는지 완벽하게 이해하지 않고서는<br>
<br>
우리가 원하는 게임 로직을 올바르게 구현하는 것이 어려울 것이다.<br>
<br>
이번 포스트에서는 `Unity` 의 "Order of Execution for Event Functions" 중 이 세가지 중요한 이벤트 메서드들의 관계에 대해 다뤄보고자 한다.<br>
<br><br>

## Update()
`Update()` 메서드는 `MonoBehavior` 에서 제공하는 기본 이벤트 메서드로, `Unity` 에서 <u>가장 일반적으로 사용되는</u> 업데이트 메서드이다. <br>
<br>
주로 게임 로직, 입력 처리, 타이머, 상태 관리 등에 사용된다. <br>
<br><br>

### Update() 호출 주기
`Update()` 메서드는 `Unity` 의 메인 루프에서 매 <b>프레임</b>마다 자동적으로 호출된다. <br>
<br>
이를 통해, 개발자는 게임 로직이나 입력 처리 같은 연속적인 작업을 구현할 수 있게 된다. <br>
<br>
`Update()` 메서드의 가장 큰 특징 중 하나는 `Frame Rate, 프레임률` 에 의존적이라는 것이다. <br>
<br>
즉, 프레임률이 높다면 `Update()` 의 호출 횟수 역시 증가하게 된다.<br>
<br>
예를 들어, 만약 게임이 `60fps` 로 실행된다면, `Update()` 메서드는 초당 약 `60` 번 호출된다. <br>
<br><br>

### Update() 의 장점
- <b>사용자 반응성 요구에 최적</b> : 매 프레임마다 호출되므로, 사용자의 반응성 요구에 대한 처리에 적합하다. <br>
즉, <u>프레임마다 변화하는</u> 게임 로직, 사용자 입력 처리, UI 변화 등에 사용하기 적합하다.<br>
특히, 사용자의 입력은 언제 들어올지 모르기 때문에 연속적으로 확인해야 하므로, 매 프레임마다 입력 상태를 확인하는 것이 좋다. <br>
애니메이션의 상태 업데이트에 대해서도, 상황에 따라 캐릭터나 오브젝트의 상태가 빠르게 변화할 수 있으므로, 매 프레임마다 이를 확인하고 갱신하는 것이 필요하다.<br>
- <b>동적 프레임률</b> : 하드웨어 성능에 따라서, 자동적으로 프레임률이 조절된다. <br>
<br><br>

### Update() 의 단점
- <b>불규칙한 호출 주기</b> : 프레임률의 변동으로 인하여, 일정한 로직 실행에는 적합하지 않다. <br>
<br><br>

### Update() 와 Time.deltaTime
게임 내에서 동작하는 많은 요소들은 프레임과 프레임 간의 시간 간격에 따라서 일정하게 조절되어야 한다. <br>
<br>
에를 들어서, 캐릭터가 일정 속도로 움직여야 한다면, 그 속도는 프레임 간의 시간에 따라서 조절되어야 한다. <br>
<br>
이 때, `Time.deltaTime` 을 활용하면, 프레임률이 떨어질 때나 프레임률이 높아질 때 모두 동일한 속도로 캐릭터가 움직일 수 있도록 해줄 수 있다.<br>
<br>
이는, `Time.deltaTime` 이 <b>이전 프레임에서 현재 프레임까지의 시간(초)</b>을 반환하기 때문인데,<br>
<br>
사용 예시는 다음과 같다. <br>
<br>

  ```c#
  float speed = 5.0f;

  void Update() {
    transform.Translate(Vector3.forward * speed * Time.deltaTime);
  }
  ```

> 게임은 다양한 하드웨어에서 실행될 수 있으므로, 일관된 게임 경험을 제공하기 위해 <b>프레임률에 영향받지 않는 연산</b>이 필요하다.

<br><br>

### Update() 의 용도
- <b>사용자 입력 반응성</b>: 실시간으로 사용자의 입력을 받아들이고, 즉각적인 피드백을 제공하는 것은 게임 경험의 핵심 중 하나이다. <br>
`Update()` 메서드는 매 프레임마다 자동으로 호출되므로, 이러한 요구에 적합하다. <br>
- <b>게임 상태와 애니메이션 상태 관리</b>: 게임 내부의 다양한 로직과 애니메이션 상태 관리는 `Update()` 메서드에서 처리하는 것이 일반적이다. <br>
예를 들어, 플레이어의 행동, 게임의 전반적인 로직 흐름 등 많은 요소들이 `Update()` 메서드 내에서 매 프레임마다 갱신될 수 있도록 해야 한다. <br>
<br><br><br>

## FixedUpdate()
`FixedUpdate()` 메서드 역시 `MonoBehavior` 에서 제공하는 기본 이벤트 메서드이다. <br>
<br>
다만, 다른 업데이트 메서드들과 비교하여 몇가지 차이점이 존재한다. <br>
<br><br>

### FixedUpdate() 호출 주기
`FixedUpdate()` 는 설정에서 지정된 고정된 간격, 즉 "Fixed Timestep"에 따라 호출된다. <br>
<br>
기본값은 약 `0.02`초 (`50fps`) 이다. (이 값은 `Time.fixedDeltaTime` 으로 조절할 수 있다.)<br>
<br>
`Update()` 메서드는 프레임률에 따라서 호출 주기가 달라지게 되므로, 물리 연산에 사용하게 되면 일관되지 않은 결과를 가져올 수 있다. <br>
<br>
물리 연산은 일정한 간격으로 처리되어야 예측 가능하고, 안정적인 결과를 얻을 수 있는데, <br>
<br>
특히, `Unity` 에서 `RigidBody` 나 `RigidBody2D` 컴포넌트의 물리 연산은 `Unity` 의 물리 엔진에 의해 관리되므로, <br>
<br>
해당 컴포넌트들은 안정적인 물리 연산을 위해서 반드시 `FixedUpdate()` 메서드 내에서 호출되어야 한다. <br>
<br>
즉, `FixedUpdate()` 메서드는 <u>주로 물리 연산을 효과적으로 처리하기 위해</u> 사용하는 것이다. <br>
<br><br>

### FixedUpdate() 의 장점
- <b>주기적 호출</b> : `FixedUpdate()` 메서드는 일정한 <b>시간</b> 간격으로 호출되기 때문에, 물리 연산과 같은 <u>규칙적이고 일정한 처리를 필요로 하는 로직</u>에 적합하다.<br>
- <b>물리 연산</b> : `Unity` 의 물리 엔진과 직접적으로 연동되므로, `Rigidbody` 와 `Rigidbody2D` 를 사용하는 물리 연산은 `FixedUpdate()` 메서드 내에서 처리해야 한다.<br>
<br><br>

### FixedUpdate() 의 단점
- <b>제한된 호출 빈도</b> : `Update()` 메서드와 다르게 매 프레임마다 호출되는 것이 아니기 때문에, 사용자 입력이나 빠른 반응이 필요한 로직에는 적합하지 않다. <br>
<br>

### FixedUpdate() 와 Upate() 의 비교
- <b>입력 지연</b> : 만약, `FixedUpdate()` 에서 사용자의 입력을 처리한다면, 입력 지연이 발생할 수 있다. <br>
이는 플레이어의 반응성을 해칠 수 있기 때문에, 사용자 입력은 `Update()` 메서드 내에서 처리하는 것이 좋다. <br>
- <b>물리 버그</b> : `Update()` 메서드 내에서 물리 연산을 처리하면 프레임률 변화에 따른 예상치 못한 물리 버그가 발생할 수 있다. <br>
따라서, 물리와 관련된 연산은 `FixedUpdate()` 메서드 내에서 처리해야 한다.<br>

<b>예시</b>
  ```c#
  public Rigidbody rb;
  public float force = 10f;

  void FixedUpdate() {
      rb.AddForce(Vector3.up * force);
  }
```
<br>

> <b>왜 `Update()` 메서드에서 물리 연산을 처리하지 않는가?</b><br>
`Update()` 메서드의 호출 빈도는 프레임률에 의존적이기 때문에 불규칙 적일 수가 있다. <br>
따라서, `Update()` 메서드에서 물리 연산을 처리하면 예측할 수 없는 결과를 초래할 수 있다.<br>
예를 들어, 높은 프레임률에서는 작은 힘의 연속적인 적용이 될 수 있고, 반대로 낮은 프레임률에서는 큰 힘의 적용이 일어날 수 있다.<br>
따라서, 일정한 호출주기를 가진 `FixedUpdate()` 메서드 내에서 예측 가능하고 일관성 있게 물리 연산을 처리해야 한다.<br>

<br>
또한, 만약 `Update()` 메서드 내에서의 애니에메이션 상태 관리와 `FixedUpdate()` 의 물리 연산이 충돌하는 경우, <br>
<br>
두 함수간의 호출 주기 차이로 인해 문제가 발생할 수 있다. <br>
<br>
이러한 경우에는 `Update()` 메서드 내에서 입력 상태를 계속 추적하고, `FixedUpdate()` 메서드 내에서 해당 상태를 체크하여 처리하여야 한다. <br>
<br>
<b>예시</b>
  ```c#
  Rigidbody rb;
  float jumpHeight = 10.0f;
  bool isJumping = false;

  void Update() {
    if (Input.GetKey(KeyCode.Space) && !isJumping)
      isJumping = true;
  }

  void FixedUpdate() {
    if (isJumping) {
      rb.AddForce(Vector3.up * jumpHeight, ForceMode.VelocityChange);
      isJumping = false;
    }
  }
```
<br><br>

### FixedUpdate() 와 Upate() 의 연동
- <b>데이터 동기화</b> : `Update()` 메서드 내에서 수집된 사용자의 입력 데이터나 게임의 상태를 `FixedUpdate()` 에서 사용해야 될 때가 있다. <br>
이럴때는, 두 함수 사이에서 데이터를 동기화 하는 방법이 필요하다.
즉, 사용자의 입력은 `Update()` 메서드 내에서 받지만, 이를 기반으로한 물리 연산은 `FixedUpdate()` 에서 수행해야 한다.<br>
입력 데이터를 임시 변수에 저장하고, `FixedUpdate()` 메서드에서 그 데이터를 사용하는 방식으로 구현할 수 있다. <br>
<br>

<b>예시</b>
```c#
  bool shouldJump = false;
  float jumpForce = 10.0f;

  void Update() {
    if (Input.GetKeyDown(KeyCode.Space))
      shouldJump = true;
  }

  void FixedUpdate() {
    if (shouldJump) {
      rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
      shouldJump = false;
    }
  }
```
<br><br><br>

## LateUpdate()
`LateUpdate()` 메서드 역시 `MonoBehavior` 에서 제공하는 기본 이벤트 메서드이다. <br>
<br>
다만, `LateUpdate()` 메서드는 `Update()` 메서드내의 모든 스크립트가 호출된 이후에 호출된다는 특징이 있다. <br>
<br><br>

### LateUpdate() 호출 주기
`LateUpdate()` 메서드 역시 `Update()` 메서드처럼 매 프레임마다 호출되며, 프레임률에 의존적이다. <br>
<br>
하지만, `LateUpdate()` 메서드는 `Update()` 메서드 내의 모든 스크립트가 호출된 후에 실행된다. <br>
<br>
이는 특정 연산이나 로직 처리를 모든 게임 객체가 자신의 상태를 갱신한 후에 수행해야 할 때 유용하다. <br>
<br>
즉, `Update()` 함수 호출 이후에 실행되므로, 다른 스크립트의 `Update()` 로직에 따른 후속 처리 작업에 적합하다. <br>
<br><br>

### LateUpdate() 의 장점
- <b>후처리 작업에 적합</b> : `Update()` 메서드로 수행된 연산 후의 작업에 적합하다. <br>
- <b>카메라 및 애니메이션 조정</b> : 오브젝트의 움직임에 따른 카메라나 오브젝트의 위치 조정에 적합하다. <br>
<br><br>

### LateUpdate() 의 단점
- <b>호출 순서</b> : 처리 순서에 민감한 로직에서는 문제가 발생할 수 있다. <br>
- <b>오버헤드</b> : `LateUpdate()` 메서드는 필요한 경우에만 사용하는 것이 좋다.<br>
불필요하게 사용하게 되면, 프레임당 처리 시간이 늘어나게 되므로 성능에 부담을 줄 수 있기 때문이다. <br>
<br><br>

### LateUpdate() 의 사용 사례
- <b>카메라 추적 시스템</b><br>
`LateUpdate()` 메서드는 플레이어나 다른 오브젝트들을 추적하는 카메라 로직에 사용되기도 한다. <br>
<br>
플레이어의 움직임이나 액션은 `Update()` 메서드에서 처리하고,<br>
<br>
그 후에 카메라가 플레이어의 위치를 기반으로 움직이게 하기 위해 `LateUpdate()` 메서드를 사용하는 것이다. <br>
<br>
이는, `Update()` 메서드에서 플레이어의 최종 위치가 결정되므로, 이 위치를 기반으로 카메라를 조절하기 위해 `LateUpdate()` 메서드가 적절하게 사용될 수 있기 때문이다. <br>
<br>

<b>예시</b>
```c#
  public Transform target; // 추적하고자 하는 대상 (예: 플레이어 자신)
  public Vector3 cameraOffset; // 대상으로부터의 카메라 위치 오프셋
  public float smoothSpeed = 0.125f; // 카메라의 부드러운 움직임을 위한 스무딩 속도
  public float moveSpeed = 5.0f; // 캐릭터의 움직임 속도

  private Camera cam; // 카메라 컴포넌트 참조

  void Start() {
    cam = Camera.main;
  }

  void Update() {
    // 플레이어 움직임 처리
    float horizontal = Input.GetAxis("Horizontal");
    float vertical = Input.GetAxis("Vertical");
    Vector3 moveDirection = new Vector3(horizontal, 0, vertical).normalized;

    transform.Translate(moveDirection * moveSpeed * Time.deltaTime, Space.World);
  }

  void LateUpdate() {
    // 카메라 추적 로직
    Vector3 desiredPosition = target.position + cameraOffset;
    Vector3 smoothedPosition = Vector3.Lerp(cam.transform.position, desiredPosition, smoothSpeed);
    cam.transform.position = smoothedPosition;
  }
```
<br>

- <b>후처리 효과와 애니메이션 연동</b><br>
또한 `LateUpdate()` 메서드는 게임 오브젝트의 애니메이션과 연동하여 특정 후처리 효과를 적용할 때도 사용된다.<br>
<br>
예를 들어, 캐릭터가 달리는 애니메이션 중 특정 시점에서 화면을 흔들거나, 기타 추가 효과들을 적용할 수 있다. <br>
<br>

<b>예시 - 카메라 무작위 흔들림 효과</b>
```c#
  public float shakeMagnitude = 0.5f;  // 흔들림의 강도
  public float shakeDuration = 1.0f;   // 흔들림 지속 시간

  private Vector3 originalPos; // 카메라의 원래 위치
  private float shakeEndTime;  // 흔들림이 끝나는 시점

  bool shouldShake = false;

  void Update() {
    if (someAnimationEventTriggered) {
      shouldShake = true;
      shakeEndTime = Time.time + shakeDuration;
      originalPos = transform.position;  // 현재 카메라 위치 저장
    }
  }

  void LateUpdate() {
    if (shouldShake) {
      if (Time.time <= shakeEndTime) {
        // 현재 카메라 위치에서 랜덤한 방향으로 shakeMagnitude만큼 움직임
        transform.position = originalPos + Random.insideUnitSphere * shakeMagnitude;
      } else {
        shouldShake = false;
        transform.position = originalPos;  // 카메라를 원래 위치로 되돌림
      }
    }
  }
```
<br><br><br>

## Update, FixedUpdate, LateUpdate 의 조화
게임 개발에서는 여러가지 로직과 이벤트들을 처리하게 된다. <br>
<br>
`Unity` 에서 이러한 처리는 주로 지금까지 다루었던 `Update()`, `FixedUpdate()` 그리고 `LateUpdate()` 의 세가지 메서드들을 통해 이루어진다. <br>
<br>
각 메서드는 각각의 특정 목적과 시기에 따라 호출되므로, 이를 고려하여 적절한 상황에서 적절하게 사용하여야 한다. <br>
<br>
- <b>연속성의 중요성</b><br>
게임의 연속성은 매우 중요하다.<br>
<br>
플레이어의 입력, 게임의 물리 연산, 그리고 그에 따른 반응이 순차적으로 처리되어야 한다. <br>
<br>
이러한 연속성을 위해 `Update()`, `FixedUpdate()` 그리고 `LateUpdate()` 가 각각의 목적에 맞게 설계된 것이다. <br>
<br>
