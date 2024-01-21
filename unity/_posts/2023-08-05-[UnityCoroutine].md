---
layout: single
title: "Unity 와 코루틴(Coroutine) - soo:bak"
date: "2023-08-05 05:40:00 +0900"
---
<br>

유니티 개발을 진행하다 보면 다양한 이벤트를 순차적으로 처리하거나 일정 시간 후에 동작을 수행하는 등의 기능을 구현해야 할 때가 많다.<br>
<br>
이러한 것들을 간편하게 구현할 수 있는 유니티의 기능 중 하나가 바로 `코루틴(Coroutine)`이다.<br>
<br>
유니티를 다루다보면 피할 수 없는, 필수적인 개념이기도 하다.<br>
<br><br>

## 코루틴(Coroutine)이란?
`코루틴(Coroutine)`은 유니티에서 일종의 비동기 처리를 위해 제공하는 기능 중 하나이다.<br>
  > 사실, 엄밀히 말하면 프레임과 프레임 사이의 코드 흐름을 제어함으로써 마치 '비동기 처리를 하는 것 처럼' 보여주는 것이다.<br>

코루틴은 일반적인 함수와는 다르게, 특정 지점에서 실행을 중지한 다음 나중에 해당 지점부터 계속 실행할 수 있는 기능을 제공하는데,<br>
<br>
이는 대기 시간을 처리하거나, 특정 조건이 충족될 때까지 기다리는 등의 상황에서 유용하게 사용된다.<br>
<br>
예를 들어, 아래의 코드는 `WaitAndPrint` 코루틴에서 `5`초 동안 대기한 후, 콘솔에 메시지를 출력한다.<br>
<br>
  ```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
  private void Start() {
    StartCoroutine(WaitAndPrint());
  }

  private IEnumerator WaitAndPrint() {
    yield return new WaitForSeconds(5);
    Debug.Log("5초 후 메시지 출력");
  }
}
  ```
<br><br>

## 코루틴과 yield return, 그리고 IEnumerator
Unity에서 코루틴은 `IEnumerator` 인터페이스를 반환하는 메서드를 통해 정의하고, `StartCoroutine` 메서드를 호출함으로써 시작된다.<br>
<br>
이 때, 코루틴의 작동 원리를 이해하기 위해서는 먼저, `yield return` 구문과 `IEnumerator` 인터페이스에 대해 알아야 한다.<br>
<br>

### yield return
`yield return` 구문은 코루틴의 핵심이라고도 할 수 있다. <br>
<br>
코루틴 내에서 해당 구문을 만나면, 코루틴은 그 시점에서 실행을 중지하고 유니티 엔진에 제어권을 넘겨주는데,<br>
<br>
이 때 코루틴의 상태와 지역변수들은 모두 유지된다.<br>
<br>
제어권을 받은 유니티 엔진은 다음 프레임에 도달하면 [IEnumerator](https://soo-bak.github.io/dev/unity/UnityCoroutine/#ienumerator) 의 `MoveNext()` 메서드를 호출하여 코루틴 실행을 재개한다.<br>
<br>
이러한 방식이 반복됨으로써 코루틴을 통한 일종의 비동기 처리가 가능해지는 것이다. <br>
<br><br>
또한, `yield return` 뒤에 올 수 있는 값에 따라서 코루틴의 흐름을 다양하게 제어할 수 있게 된다. <br>
<br>
 - `yield return null` : 다음 프레임까지 코루틴을 중지하고 대기
 - `yield return new WaitForSeconds(float seconds)` : 지정된 초 만큼 코루틴을 중지하고 대기
 - `yield return new WaitForFixedUpdate()` : 다음 `FixedUpdate` 까지 코루틴을 중지하고 대기
 - `yield return new WaitForSecondsRealtime(float seconds)` : 실제 시간으로 지정된 초 만큼 코루틴을 중지하고 대기<br>(즉, 유니티의 `TimeScale` 이 `0` 인 상태에서도 대기 시간이 흐른다.)
 - `yield return new WaitUntill(Func<bool> predicate)` : 특정 조건이 참이 될 때까지 코루틴을 중지하고 대기
 - `yield return StartCoroutine(IEnumerator method)` : 다른 코루틴이 완료될 때 까지 해당 코루틴을 중지하고 대기
 - `...`
<br><br><br>

### IEnumerator


<br>
`IEnumerator` 인터페이스는 `C#` 의 `.NET Framework`에서 제공하는 인터페이스로 `System.Collections` 네임스페이스 안에 다음과 같이 정의되어 있다.<br>
<br>
  ```c#
public interface IEnumerator {
  object Current { get; }
  bool MoveNext();
  void Reset();
}
  ```
  - `Current` : 컬렉션의 현재 요소를 반환한다.<br>
  - `MoveNext()` : 컬렉션의 다음 요소로 이동한다. 다음 요소가 있으면 `true` 를, 그렇지 않으면 `false` 를 반환한다.<br>
  - `Reset()` : 컬렉션의 처음으로 다시 이동한다. <br>
<br>

유니티는 코루틴의 진행에 해당 인터페이스를 사용한다. <br>
<br>
코루틴이 시작되면, 유니티 엔진은 `MoveNext()` 메서드를 호출하여 코루틴을 실행하고,<br>
<br>
`yield return` 구문을 만났을 때 현재 태를 `Current` 프로퍼티에 저장한다음 코루틴을 중지 후 대기한다.<br>
<br>
`Reset()` 메서드는 유니티의 코루틴에서는 사용되지 않는다.<br>
<br><br>
이렇게 `IEnumerator` 인터페이스는 유니티에서 `Current` 프로퍼티를 통해 코루틴의 상태를 저장하고,<br>
<br>
`yield return` 구문과 `MoveNext()` 메서드를 통해 코루틴의 진행을 제어할 수 있도록 해주는 것이다.<br>
<br><br>

## 코루틴의 제어

### 코루틴 시작하기
코루틴을 시작하기 위해서는 `StartCoroutine()` 메서드를 사용한다.<br>
<br>
이 메서드는 코루틴 함수의 이름(`string`) 또는 `IEnumerator` 객체를 인수로 받는다.<br>
<br>
  - 예시<br>

  ```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
  private void Start() {
    StartCoroutine("WaitAndPrint");
  }

  private IEnumerator WaitAndPrint() {
    yield return new WaitForSeconds(5);
    Debug.Log("5초 후 메시지 출력");
  }
}
  ```
<br>

### 코루틴 멈추기
코루틴을 임의로 중지하기 위해서는 `StopCoroutine()` 메서드를 사용한다. <br>
<br>
이 메서드 역시 `StartCoroutine()` 메서드와 마찬가지로, 이름(`string`) 또는 `IEnumerator` 객체를 인수로 받는다.<br>
<br>
  - 예시<br>

  ```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
  private void Start() {
    StartCoroutine("WaitAndPrint");
    // 2초 후 코루틴이 멈추도록 Invoke
    Invoke("StopExampleCoroutine", 2f);
  }

  private IEnumerator WaitAndPrint() {
    yield return new WaitForSeconds(5);
    Debug.Log("5초 후 메시지 출력");
  }

  private void StopExampleCoroutine() {
    StopCoroutine("WaitAndPrint");
    Debug.Log("코루틴 중지!");
  }
}
  ```
<br>

### 모든 코루틴 멈추기
유니티 엔진에서 실행되고 있는 모든 코루틴을 한 번에 중지하기 위해 `StopAllCoroutines()` 메서드를 사용할 수도 있다. <br>
<br>
해당 메서드는 특정 인수를 필요로 하지 않는다.<br>
<br>
  - 예시<br>

  ```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
  private void Start() {
    StartCoroutine("WaitAndPrint_1");
    StartCoroutine("WaitAndPrint_2");
    // 2초 후 모든 코루틴 한 번에 멈추기
    Invoke("StopAllExampleCoroutine", 2f);
  }

  private IEnumerator WaitAndPrint_1() {
    yield return new WaitForSeconds(5);
    Debug.Log("5초 후 메시지 출력");
  }

  private IEnumerator WaitAndPrint_2() {
    yield return new WaitForSeconds(10);
    Debug.Log("10초 후 메시지 출력");
  }

  private void StopAllExampleCoroutine() {
    StopAllCoroutines();
    Debug.Log("모든 코루틴 중지!");
  }
}
  ```
<br><br>

## 코루틴과 async/await
코루틴과 `async/await` 는 비슷하면서도 주요한 차이점들이 있다. <br>
<br>
그 중 가장 큰 차이점은 코루틴은 유니티의 <b>메인 스레드</b>에서 실행되지만, `async/await` 는 <b>별도의 스레드</b>에서 실행된다는 점이다.<br>
<br>
즉, 코루틴 작업은 모든 것이 <u>메인 스레드에서 순차적으로 실행</u>되므로, 엄밀히 말하면 "비동기 스타일" 코드를 작성하는 것을 돕지만,<br>
<br>
<b>실제로 병렬 처리를 수행하지는 않는 것</b>이다.<br>
<br>
따라서, 무거운 작업이나 비용이 큰 작업을 코루틴 내에서 수행하게되면 게임의 프레임률이 떨어지게 된다.<br>
<br><br>
또한, `async/await` 는 별도의 스레드에서 실행되므로,<br>
<br>
`async/await` 를 통해 유니티의 메인 스레드에서만 수행할 수 있는 작업, 예를 들어 UI 업데이트나 게임오브젝트 조작 등을 처리하려면,<br>
<br>
`SynchronizationContext` 를 활용하거나, 메인 스레드에서 작업을 처리할 수 있도록 별도의 처리 코드를 명시적으로 작성해야 한다.<br>
<br>
그렇지 않으면, `Unity API` 들을 안전하게 호출할 수 없다.<br>
<br>
  - 예시<br>

  ```c#
async Task AsyncAwaitExample() {
  await Task.Run(() => {
      // 이 부분은 백그라운드 스레드에서 실행되므로, 게임 오브젝트를 직접 조작하면 안 된다.
  });

  // 메인 스레드에서 실행되어야 하는 코드는 다음과 같이 처리해야 한다.
  await UnityMainThreadDispatcher.Instance.Enqueue(() => {
      GameObject obj = new GameObject("MyObject");
  });
}
  ```
<br>
반면, 코루틴 내에서는 모든 `Unity API` 를 자유롭게 사용해도 된다.<br>
<br><br><br>
또한, 코루틴은 예외가 발생하면 즉시 중단되는 반면, `async/await` 는 `try-catch` 블록을 활용하여 예외처리를 보다 쉽게 할 수 있다.<br>
<br>
  - 예시<br>

  ```c#
public async Task ExceptionHandlingExample() {
  try {
    await Task.Run(() => {
      throw new Exception("예외 발생");
    });
  } catch (Exception ex) {
      Debug.Log("예외 발생: " + ex.Message);
  }
}
  ```
<br>
<br><br><br>
그리고, `async/await` 는 `Task<T>` 를 반환할 수 있으므로, 비동기 작업의 결과를 보다 간편하게 처리할 수 있다.<br>
<br>
  - 예시<br>

  ```c#
public async Task<int> CalculateSumAsync(int a, int b) {
  return await Task.Run(() => {
    return a + b;
  });
}

public async Task ExampleUsage() {
  int result = await CalculateSumAsync(5, 7);
  Debug.Log("결과: " + result);
}
  ```
<br><br>
이렇게 `async/await` 사용의 장점들이 있지만,<br>
<br>
코루틴은<br>
  - `Unity API` 를 자유롭게 사용할 수 있다는 점 <br>
  - `yield return` 을 통해 특정 시간 동안 대기하거나, 다음 프레임까지 기다리는 작업, 특정 조건을 만족할 때까지 대기하는 작업 등을 쉽게 처리할 수 있다는 점<br>
  - 간편하게 사용이 가능하다는 점<br>
<br>

등의 장점이 있다.<br>
<br>
따라서, 코루틴과 `async/await` 는 각각의 특징과 상황에 맞게 적절히 사용해야 한다.<br>
<br>
