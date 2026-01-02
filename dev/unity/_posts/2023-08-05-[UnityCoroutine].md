---
layout: single
title: "Unity 와 코루틴(Coroutine) - soo:bak"
date: "2023-08-05 05:40:00 +0900"
description: "Unity 코루틴의 개념, 동작 원리, yield return과 IEnumerator, async/await와의 비교, 비동기와 병렬의 차이를 정확하게 설명합니다."
tags:
  - Unity
  - 코루틴
  - Coroutine
  - C#
  - 게임 개발
  - 비동기
keywords: "Unity 코루틴, Coroutine, yield return, IEnumerator, StartCoroutine, 비동기 처리, 병렬 처리, async await, Unity 게임 개발"
---
<br>

유니티 개발을 진행하다 보면 다양한 이벤트를 순차적으로 처리하거나 일정 시간 후에 동작을 수행하는 등의 기능을 구현해야 할 때가 많다.<br>
<br>
이러한 것들을 간편하게 구현할 수 있는 유니티의 기능 중 하나가 바로 `코루틴(Coroutine)`이다.<br>
<br>
유니티를 다루다보면 피할 수 없는, 필수적인 개념이기도 하다.<br>
<br><br>

## 비동기(Asynchronous)와 병렬(Parallel)의 차이

코루틴을 이해하기 전에, 먼저 <b>비동기</b>와 <b>병렬</b>의 차이를 명확히 이해해야 한다.<br>
<br>
이 두 개념은 자주 혼동되지만, 완전히 다른 의미를 가진다.<br>
<br>

### 동기(Synchronous) vs 비동기(Asynchronous)
<b>동기 처리</b>는 작업이 완료될 때까지 다음 코드의 실행을 <u>기다리는</u> 방식이다.<br>
<br>
<b>비동기 처리</b>는 작업이 완료될 때까지 기다리지 않고, 일단 <u>제어권을 양보</u>한 뒤 나중에 결과를 받는 방식이다.<br>
<br>

```c#
// 동기 처리: 파일 읽기가 완료될 때까지 대기
string content = File.ReadAllText("file.txt");
Debug.Log("파일 읽기 완료");  // 파일 읽기가 끝나야 실행됨

// 비동기 처리: 파일 읽기를 요청하고 제어권 양보
var task = File.ReadAllTextAsync("file.txt");
Debug.Log("파일 읽기 요청함");  // 파일 읽기 완료 전에 실행됨
string content = await task;   // 여기서 결과를 기다림
```
<br>

### 단일 스레드 vs 병렬(멀티 스레드)
<b>병렬 처리</b>는 여러 작업을 <u>동시에 여러 스레드(또는 CPU 코어)에서</u> 실행하는 것이다.<br>
<br>
중요한 점은, <b>비동기가 반드시 병렬을 의미하지는 않는다</b>는 것이다.<br>
<br>

```
비동기 + 단일 스레드:
┌─────────────────────────────────────────┐
│  메인 스레드                              │
│  ┌──────┐     ┌──────┐     ┌──────┐     │
│  │작업 A│ ──→ │작업 B│ ──→ │작업 A│     │
│  │시작  │     │실행  │     │재개  │     │
│  └──────┘     └──────┘     └──────┘     │
│      ↓ 제어권 양보    ↓ 제어권 양보        │
└─────────────────────────────────────────┘

병렬 (멀티 스레드):
┌─────────────────────────────────────────┐
│  스레드 1: ████████████ 작업 A           │
│  스레드 2: ████████████ 작업 B           │
│  스레드 3: ████████████ 작업 C           │
│  (동시에 실행)                            │
└─────────────────────────────────────────┘
```
<br>

이제 코루틴이 어디에 해당하는지 알 수 있다.<br>
<br>
<b>코루틴은 단일 스레드에서 동작하는 비동기 패턴이다.</b><br>
<br><br>

## 코루틴(Coroutine)이란?
`코루틴(Coroutine)`은 실행을 일시 중단하고 나중에 재개할 수 있는 함수이다.<br>
<br>
일반적인 함수는 호출되면 처음부터 끝까지 한 번에 실행되지만,<br>
<br>
코루틴은 특정 지점에서 실행을 <b>중단(yield)</b>하고, 나중에 그 지점부터 다시 <b>재개(resume)</b>할 수 있다.<br>
<br>

```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
    private void Start() {
        StartCoroutine(WaitAndPrint());
    }

    private IEnumerator WaitAndPrint() {
        Debug.Log("1. 코루틴 시작");
        yield return new WaitForSeconds(2);  // 여기서 중단, 2초 후 재개
        Debug.Log("2. 2초 후 실행");
        yield return new WaitForSeconds(1);  // 여기서 중단, 1초 후 재개
        Debug.Log("3. 1초 더 후 실행");
    }
}
```
<br>

위 코드에서 `yield return` 을 만나면 코루틴은 실행을 중단하고 유니티 엔진에 제어권을 돌려준다.<br>
<br>
그 사이에 유니티는 다른 게임 로직을 처리하고, 지정된 시간이 지나면 코루틴 실행을 재개한다.<br>
<br>
<b>이 모든 과정이 메인 스레드에서 일어난다.</b><br>
<br>
따라서 코루틴은 게임을 멈추지 않으면서도 시간 기반 로직을 쉽게 구현할 수 있게 해주는 것이다.<br>
<br><br>

### 코루틴이 병렬 처리가 아닌 이유
코루틴 내에서 무거운 연산을 수행하면 게임이 버벅거리게 된다.<br>
<br>
왜냐하면 코루틴은 메인 스레드에서 실행되기 때문이다.<br>
<br>

```c#
private IEnumerator HeavyWork() {
    // 이 루프가 실행되는 동안 게임이 멈춘다!
    for (int i = 0; i < 10000000; i++) {
        DoSomeCalculation(i);
    }
    yield return null;
}
```
<br>

코루틴은 "시간을 분할해서 작업을 나눠서 실행"하는 것이지, "다른 스레드에서 동시에 실행"하는 것이 아니다.<br>
<br>

```c#
// 올바른 사용: 작업을 여러 프레임에 분산
private IEnumerator HeavyWorkDistributed() {
    for (int i = 0; i < 10000000; i++) {
        DoSomeCalculation(i);

        // 100번 연산마다 한 프레임 양보
        if (i % 100 == 0) {
            yield return null;
        }
    }
}
```
<br><br>

## 코루틴과 yield return, 그리고 IEnumerator

Unity 에서 코루틴은 `IEnumerator` 인터페이스를 반환하는 메서드를 통해 정의하고, `StartCoroutine` 메서드를 호출함으로써 시작된다.<br>
<br>
이 때, 코루틴의 작동 원리를 이해하기 위해서는 먼저, `yield return` 구문과 `IEnumerator` 인터페이스에 대해 알아야 한다.<br>
<br>

### yield return
`yield return` 구문은 코루틴의 핵심이라고도 할 수 있다.<br>
<br>
코루틴 내에서 해당 구문을 만나면, 코루틴은 그 시점에서 실행을 중지하고 유니티 엔진에 제어권을 넘겨주는데,<br>
<br>
이 때 코루틴의 상태와 지역변수들은 모두 유지된다.<br>
<br>
제어권을 받은 유니티 엔진은 조건이 충족되면 [IEnumerator](#ienumerator) 의 `MoveNext()` 메서드를 호출하여 코루틴 실행을 재개한다.<br>
<br>
이러한 방식이 반복됨으로써 코루틴을 통한 비동기 처리가 가능해지는 것이다.<br>
<br><br>
또한, `yield return` 뒤에 올 수 있는 값에 따라서 코루틴의 흐름을 다양하게 제어할 수 있게 된다.<br>
<br>
 - `yield return null` : 다음 프레임까지 코루틴을 중지하고 대기
 - `yield return new WaitForSeconds(float seconds)` : 지정된 초 만큼 코루틴을 중지하고 대기
 - `yield return new WaitForFixedUpdate()` : 다음 `FixedUpdate` 까지 코루틴을 중지하고 대기
 - `yield return new WaitForSecondsRealtime(float seconds)` : 실제 시간으로 지정된 초 만큼 코루틴을 중지하고 대기<br>(즉, 유니티의 `TimeScale` 이 `0` 인 상태에서도 대기 시간이 흐른다.)
 - `yield return new WaitUntil(Func<bool> predicate)` : 특정 조건이 참이 될 때까지 코루틴을 중지하고 대기
 - `yield return new WaitWhile(Func<bool> predicate)` : 특정 조건이 거짓이 될 때까지 코루틴을 중지하고 대기
 - `yield return StartCoroutine(IEnumerator routine)` : 다른 코루틴이 완료될 때까지 해당 코루틴을 중지하고 대기
 - `yield return new WaitForEndOfFrame()` : 현재 프레임의 렌더링이 완료될 때까지 대기
 - `yield break` : 코루틴을 즉시 종료
<br><br><br>

### IEnumerator

`IEnumerator` 인터페이스는 `C#` 의 `.NET Framework` 에서 제공하는 인터페이스로 `System.Collections` 네임스페이스 안에 다음과 같이 정의되어 있다.<br>
<br>

```c#
public interface IEnumerator {
    object Current { get; }
    bool MoveNext();
    void Reset();
}
```
  - `Current` : 현재 yield 된 값을 반환한다.<br>
  - `MoveNext()` : 다음 yield 지점까지 코드를 실행한다. 더 실행할 코드가 있으면 `true` 를, 그렇지 않으면 `false` 를 반환한다.<br>
  - `Reset()` : 유니티의 코루틴에서는 사용되지 않는다.<br>
<br>

유니티는 코루틴의 진행에 해당 인터페이스를 사용한다.<br>
<br>
코루틴이 시작되면, 유니티 엔진은 `MoveNext()` 메서드를 호출하여 첫 번째 `yield return` 까지 실행하고,<br>
<br>
`yield return` 구문을 만나면 반환된 값을 `Current` 프로퍼티에 저장한 다음 코루틴을 중지한다.<br>
<br>
유니티는 `Current` 값을 확인하여 언제 다시 `MoveNext()` 를 호출할지 결정한다.<br>
<br>

```
코루틴 실행 흐름:
1. StartCoroutine(MyCoroutine()) 호출
2. 유니티가 MoveNext() 호출 → 첫 yield return까지 실행
3. Current 값 확인 (예: WaitForSeconds(2))
4. 2초 대기...
5. 유니티가 MoveNext() 호출 → 다음 yield return까지 실행
6. MoveNext()가 false 반환할 때까지 반복
```
<br><br>

## 코루틴의 제어

### 코루틴 시작하기
코루틴을 시작하기 위해서는 `StartCoroutine()` 메서드를 사용한다.<br>
<br>
이 메서드는 `IEnumerator` 객체 또는 코루틴 함수의 이름(`string`)을 인수로 받는다.<br>
<br>

```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
    private Coroutine runningCoroutine;

    private void Start() {
        // 방법 1: IEnumerator 직접 전달 (권장)
        runningCoroutine = StartCoroutine(WaitAndPrint());

        // 방법 2: 문자열로 전달 (비권장 - 오타 위험, 성능 저하)
        StartCoroutine("WaitAndPrint");
    }

    private IEnumerator WaitAndPrint() {
        yield return new WaitForSeconds(5);
        Debug.Log("5초 후 메시지 출력");
    }
}
```
<br>

`StartCoroutine()` 은 `Coroutine` 객체를 반환하는데, 이를 저장해두면 나중에 해당 코루틴만 정확히 중지할 수 있다.<br>
<br>

### 코루틴 멈추기
코루틴을 임의로 중지하기 위해서는 `StopCoroutine()` 메서드를 사용한다.<br>
<br>

```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
    private Coroutine runningCoroutine;

    private void Start() {
        runningCoroutine = StartCoroutine(WaitAndPrint());
        Invoke("StopExampleCoroutine", 2f);
    }

    private IEnumerator WaitAndPrint() {
        yield return new WaitForSeconds(5);
        Debug.Log("5초 후 메시지 출력");
    }

    private void StopExampleCoroutine() {
        // 방법 1: Coroutine 객체로 중지 (권장)
        if (runningCoroutine != null) {
            StopCoroutine(runningCoroutine);
        }

        // 방법 2: 문자열로 중지 (문자열로 시작한 경우에만)
        // StopCoroutine("WaitAndPrint");

        Debug.Log("코루틴 중지!");
    }
}
```
<br>

주의할 점은, `IEnumerator` 객체로 시작한 코루틴은 문자열로 중지할 수 없고, 그 반대도 마찬가지라는 것이다.<br>
<br>
따라서 `Coroutine` 객체를 저장해두고 이를 통해 중지하는 것이 가장 확실한 방법이다.<br>
<br>

### 모든 코루틴 멈추기
해당 `MonoBehaviour` 에서 실행 중인 모든 코루틴을 한 번에 중지하기 위해 `StopAllCoroutines()` 메서드를 사용할 수 있다.<br>
<br>

```c#
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour {
    private void Start() {
        StartCoroutine(WaitAndPrint_1());
        StartCoroutine(WaitAndPrint_2());
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
<br>

`StopAllCoroutines()` 는 해당 `MonoBehaviour` 컴포넌트에서 시작된 코루틴만 중지한다.<br>
<br>
다른 게임 오브젝트나 다른 컴포넌트의 코루틴에는 영향을 주지 않는다.<br>
<br><br>

## 코루틴과 async/await

코루틴과 `async/await` 는 모두 비동기 프로그래밍을 위한 도구이지만, 동작 방식에 차이가 있다.<br>
<br>

### async/await 는 스레드를 생성하지 않는다
흔히 오해하는 부분인데, <b>`async/await` 는 자동으로 별도의 스레드를 생성하지 않는다.</b><br>
<br>
`async/await` 는 비동기 프로그래밍 <b>패턴</b>이지, 멀티스레딩 도구가 아니다.<br>
<br>

```c#
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class AsyncExample : MonoBehaviour {
    async void Start() {
        Debug.Log($"1. 시작 - Thread: {Thread.CurrentThread.ManagedThreadId}");

        await Task.Delay(1000);  // 1초 대기

        // Unity에서는 여전히 메인 스레드!
        Debug.Log($"2. 1초 후 - Thread: {Thread.CurrentThread.ManagedThreadId}");

        // Unity API 사용 가능
        transform.position = Vector3.zero;
    }
}

// 출력:
// 1. 시작 - Thread: 1
// 2. 1초 후 - Thread: 1
```
<br>

Unity 에서 `async/await` 를 사용하면, `await` 이후에도 기본적으로 <b>메인 스레드로 돌아온다.</b><br>
<br>
이는 Unity 의 `UnitySynchronizationContext` 가 `await` 이후 메인 스레드에서 실행을 재개하도록 보장하기 때문이다.<br>
<br>

### 별도 스레드를 사용하려면 명시적으로 요청해야 한다
`Task.Run()` 을 사용하면 명시적으로 스레드 풀의 스레드에서 작업을 실행할 수 있다.<br>
<br>

```c#
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class ThreadExample : MonoBehaviour {
    async void Start() {
        Debug.Log($"1. 메인 스레드: {Thread.CurrentThread.ManagedThreadId}");

        int result = await Task.Run(() => {
            // 이 부분은 스레드 풀의 별도 스레드에서 실행
            Debug.Log($"2. 워커 스레드: {Thread.CurrentThread.ManagedThreadId}");
            return HeavyCalculation();
        });

        // Unity에서는 다시 메인 스레드로 돌아옴
        Debug.Log($"3. 다시 메인 스레드: {Thread.CurrentThread.ManagedThreadId}");

        // Unity API 사용 가능
        Debug.Log($"계산 결과: {result}");
    }

    private int HeavyCalculation() {
        // 무거운 연산...
        return 42;
    }
}

// 출력:
// 1. 메인 스레드: 1
// 2. 워커 스레드: 7  (다른 스레드!)
// 3. 다시 메인 스레드: 1
```
<br>

`Task.Run()` 내부에서는 Unity API 를 호출하면 안 된다.<br>
<br>
Unity API 는 메인 스레드에서만 안전하게 호출할 수 있기 때문이다.<br>
<br>

### 코루틴 vs async/await 비교

| 항목 | 코루틴 | async/await |
|------|--------|-------------|
| 실행 스레드 | 항상 메인 스레드 | 기본적으로 메인 스레드 (Task.Run 사용 시 별도 스레드) |
| Unity API 사용 | 항상 가능 | await 이후 가능 (Task.Run 내부에서는 불가) |
| 프레임 기반 대기 | `yield return null` 등 직관적 | `await Task.Yield()` (권장되지 않음) |
| 시간 기반 대기 | `WaitForSeconds` (TimeScale 영향) | `Task.Delay` (실제 시간) |
| 반환값 | 불가 (`IEnumerator`) | 가능 (`Task<T>`) |
| 예외 처리 | 어려움 (예외 시 중단) | `try-catch` 사용 가능 |
| 취소 | `StopCoroutine` | `CancellationToken` |
| GC 할당 | YieldInstruction 생성 시 발생 | Task 생성 시 발생 (UniTask 사용 시 최소화) |
<br>

### UniTask: Unity 에 최적화된 async/await
표준 `Task` 는 Unity 에 최적화되어 있지 않아 GC 할당이 발생하고, `WaitForSeconds` 같은 Unity 전용 대기를 지원하지 않는다.<br>
<br>
[UniTask](https://github.com/Cysharp/UniTask) 는 이러한 문제를 해결한 Unity 전용 비동기 라이브러리이다.<br>
<br>

```c#
using Cysharp.Threading.Tasks;

public class UniTaskExample : MonoBehaviour {
    async UniTaskVoid Start() {
        // Unity의 시간 시스템과 연동
        await UniTask.Delay(1000);  // 1초 대기

        // WaitForSeconds처럼 TimeScale 영향 받음
        await UniTask.Delay(TimeSpan.FromSeconds(1), DelayType.DeltaTime);

        // 프레임 대기
        await UniTask.Yield();
        await UniTask.NextFrame();

        // 조건 대기
        await UniTask.WaitUntil(() => someCondition);
    }
}
```
<br>

UniTask 는 코루틴의 편리함과 `async/await` 의 장점을 모두 제공하므로, UniTask 사용을 고려해볼 만 하다.<br>
<br><br>

## 언제 무엇을 사용해야 하는가?

### 코루틴이 적합한 경우
- 간단한 시간 기반 로직 (페이드 인/아웃, 연출 등)
- Unity 의 프레임 사이클과 밀접한 작업
- 기존 코드베이스가 코루틴 기반인 경우
<br>

### async/await 가 적합한 경우
- 반환값이 필요한 비동기 작업
- 외부 API 호출, 파일 I/O 등 진정한 비동기 작업
- 복잡한 예외 처리가 필요한 경우
- 병렬 처리가 필요한 경우 (`Task.Run` 활용)
<br>

### 진정한 병렬 처리가 필요한 경우
CPU 집약적인 작업을 백그라운드에서 처리해야 한다면 `Task.Run` 을 사용한다.<br>
<br>

```c#
using System.Threading.Tasks;

async void ProcessLargeData() {
    // 무거운 연산을 백그라운드 스레드에서 실행
    var result = await Task.Run(() => {
        // 이 블록은 별도 스레드에서 실행됨
        // Unity API 호출 금지!
        return PerformHeavyCalculation();
    });

    // 메인 스레드로 돌아와서 결과 사용
    Debug.Log($"결과: {result}");
    UpdateUI(result);
}
```
<br><br>

## 결론
코루틴은 <b>단일 스레드에서 동작하는 비동기 패턴</b>이다.<br>
<br>
병렬 처리가 아니므로 무거운 연산을 코루틴에서 실행하면 게임이 버벅거린다.<br>
<br>
`async/await` 도 기본적으로는 메인 스레드에서 실행되며, `Task.Run()` 을 명시적으로 사용해야만 별도 스레드에서 작업이 실행된다.<br>
<br>
각 도구의 특성을 정확히 이해하고, 상황에 맞게 적절히 사용하는 것이 중요하다.<br>
<br>

---

### 참고 자료
- [Unity 공식 문서 - Coroutines](https://docs.unity3d.com/Manual/Coroutines.html)
- [Unity 공식 문서 - Order of Execution](https://docs.unity3d.com/Manual/ExecutionOrder.html)
- [UniTask - GitHub](https://github.com/Cysharp/UniTask)
- [Microsoft Docs - Async/Await](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/async/)
