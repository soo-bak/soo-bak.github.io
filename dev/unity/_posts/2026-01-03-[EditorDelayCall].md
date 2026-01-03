---
layout: single
title: "Unity Editor 의 DelayCall 심층 분석 - soo:bak"
date: "2026-01-03 09:00:00 +0900"
description: "Unity Editor의 EditorApplication.delayCall 동작 원리, InitializeOnLoad와의 관계, 실제 오픈소스 컨트리뷰션 사례를 통한 활용법을 상세히 분석합니다."
pin: true
tags:
  - Unity
  - Editor
  - DelayCall
  - C#
  - 게임 개발
  - 오픈소스
keywords: "Unity Editor, EditorApplication.delayCall, InitializeOnLoad, 도메인 리로드, Steamworks.NET, 에디터 확장, Unity 6"
---
<br>

Unity 에서 런타임 환경의 비동기 처리에는 [코루틴(Coroutine)](https://soo-bak.github.io/dev/unity/UnityCoroutine/)이 널리 사용된다.<br>
<br>
Unity 에디터 환경에서도 비슷한 개념이 있다.<br>
<br>
에디터 스크립트를 작성하다 보면 특정 작업을 "지금 당장"이 아닌 "안전한 시점"에 실행해야 할 때가 있는데,<br>
<br>
이럴 때 사용하는 것이 바로 `EditorApplication.delayCall` 이다.<br>
<br><br>

## EditorApplication.delayCall 이란?
`EditorApplication.delayCall` 은 Unity 에디터가 현재 프레임의 모든 처리를 완료한 후, 다음 에디터 업데이트 시점에 콜백을 실행하도록 예약하는 메커니즘이다.<br>
<br>

```c#
using UnityEditor;

public class DelayCallExample
{
    [InitializeOnLoadMethod]
    static void Initialize()
    {
        EditorApplication.delayCall += () => {
            UnityEngine.Debug.Log("에디터가 안정된 후 실행됩니다.");
        };
    }
}
```
<br>

여기서 핵심은 <b>"안정된 시점"</b> 이다.<br>
<br>
Unity 에디터는 스크립트 컴파일, 도메인 리로드, 에셋 임포트 등 다양한 내부 작업을 수행하는데,<br>
<br>
이러한 작업들이 진행 중일 때 특정 API 를 호출하면 예상치 못한 동작이 발생할 수 있다.<br>
<br>
`delayCall` 은 이런 내부 작업들이 완료된 후 안전하게 코드를 실행할 수 있도록 해준다.<br>
<br><br>

## Unity 에디터의 라이프사이클 이해

`delayCall` 을 제대로 활용하려면 Unity 에디터의 라이프사이클에 대한 이해가 필요하다.<br>
<br>

### 에디터 업데이트 루프
Unity 에디터는 런타임의 게임 루프와는 별개로, 자체적인 업데이트 루프를 가지고 있다.<br>
<br>
이 루프에서 `delayCall` 은 Unity 공식 문서에 따르면 <b>"모든 인스펙터 업데이트가 완료된 후"</b> 실행된다.<br>
<br>

```
에디터 업데이트 사이클:
- 이벤트 처리 (마우스, 키보드, GUI 이벤트)
- EditorApplication.update 콜백 실행
- 인스펙터 업데이트
- EditorApplication.delayCall 콜백 실행 (있을 경우)
- GUI 렌더링
```
<br>

여기서 중요한 점은 `delayCall` 콜백이 현재 프레임의 주요 처리가 끝난 후에 실행된다는 것이다.<br>
<br>
즉, 도메인 리로드나 컴파일이 진행 중인 불안정한 시점이 아닌, 에디터가 안정된 상태에서 실행된다.<br>
<br><br>

### 도메인 리로드 (Domain Reload) 의 내부 동작
도메인 리로드는 Unity 가 C# 스크립트 환경을 완전히 재설정하는 과정이다.<br>
<br>
이 과정은 단순히 스크립트를 다시 로드하는 것이 아니라, AppDomain 전체를 재생성하는 무거운 작업이다.<br>
<br>

```
도메인 리로드 순서:
1. 기존 AppDomain 언로드
   - 모든 정적 변수 초기화
   - 등록된 이벤트 핸들러 해제
   - 관리되는 리소스 정리

2. 새 AppDomain 생성
   - 어셈블리 로드
   - 타입 정보 초기화

3. 초기화 콜백 실행
   - [InitializeOnLoad] 정적 생성자 호출
   - [InitializeOnLoadMethod] 메서드 호출

4. 에디터 상태 복원
   - 직렬화된 데이터 역직렬화
   - EditorWindow 상태 복원
```
<br>

도메인 리로드가 발생하는 상황은 다음과 같다.<br>
<br>
- 스크립트 파일 변경 및 컴파일
- 플레이 모드 진입/종료 (Enter Play Mode Options 설정에 따라 다름)
- 에셋 임포트로 인한 스크립트 변경
- 스크립팅 정의 기호(Scripting Define Symbols) 변경
- 어셈블리 정의 파일(.asmdef) 변경
<br><br>

### InitializeOnLoad 의 실행 시점
`[InitializeOnLoad]` 어트리뷰트는 Unity 에디터가 시작되거나 스크립트가 리컴파일될 때 정적 생성자를 자동으로 호출하도록 한다.<br>
<br>

```c#
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
public class AutoInitializer
{
    static AutoInitializer()
    {
        Debug.Log("에디터 시작 또는 리컴파일 시 자동 실행");
    }
}
```
<br>

여기서 중요한 점은, 정적 생성자가 호출되는 시점이 도메인 리로드 과정의 <b>초기 단계</b>라는 것이다.<br>
<br>
즉, 이 시점에서는 아직 에디터의 모든 시스템이 완전히 초기화되지 않은 상태이다.<br>
<br>

```
[InitializeOnLoad] 실행 시점의 상태:
- 어셈블리 로드: 완료
- 타입 정보: 사용 가능
- EditorWindow: 복원 중
- AssetDatabase: 갱신 중일 수 있음
- 컴파일 파이프라인: 아직 완료되지 않았을 수 있음
```
<br>

이러한 불안정한 상태에서 특정 작업을 수행하면 예상치 못한 동작이 발생할 수 있다.<br>
<br><br>

## delayCall 의 내부 구현과 타이밍

### 콜백 큐 시스템
`EditorApplication.delayCall` 은 내부적으로 콜백 큐 시스템을 사용한다.<br>
<br>

```c#
// Unity 내부 구현을 단순화한 의사 코드
internal static class EditorApplicationInternal
{
    private static Queue<Action> delayCallQueue = new Queue<Action>();

    public static void AddDelayCall(Action callback)
    {
        delayCallQueue.Enqueue(callback);
    }

    internal static void ProcessDelayedCalls()
    {
        while (delayCallQueue.Count > 0)
        {
            var callback = delayCallQueue.Dequeue();
            try
            {
                callback?.Invoke();
            }
            catch (Exception e)
            {
                Debug.LogException(e);
            }
        }
    }
}
```
<br>

이 시스템의 특징은 다음과 같다.<br>
<br>
- <b>FIFO (First In, First Out)</b>: 등록된 순서대로 실행된다.
- <b>일회성</b>: 실행된 콜백은 큐에서 제거된다.
- <b>예외 안전</b>: 하나의 콜백에서 예외가 발생해도 다른 콜백은 계속 실행된다.
- <b>프레임 독립적</b>: 한 프레임에서 여러 개의 delayCall 이 등록되어도 모두 다음 프레임에 순차 실행된다.
<br><br>

### delayCall 과 update 의 실행 순서
`EditorApplication.update` 와 `delayCall` 의 실행 순서를 이해하는 것이 중요하다.<br>
<br>

```c#
[InitializeOnLoad]
public class ExecutionOrderTest
{
    static ExecutionOrderTest()
    {
        EditorApplication.update += () => Debug.Log("update 호출");
        EditorApplication.delayCall += () => Debug.Log("delayCall 호출");
    }
}

// 출력:
// update 호출
// delayCall 호출  ← 첫 번째 사이클에서 한 번만 실행
// update 호출
// update 호출
// ...
```
<br>

`delayCall` 은 등록 직후의 다음 업데이트 사이클에서 <b>한 번만</b> 실행되고,<br>
<br>
`update` 는 매 에디터 프레임마다 계속 실행된다는 차이가 있다.<br>
<br><br>

## Steamworks.NET 오픈소스 기여를 통해 배운 것

[Steamworks.NET](https://github.com/rlabrecque/Steamworks.NET) 은 Steam API 를 Unity 에서 사용할 수 있게 해주는 널리 사용되는 오픈소스 라이브러리이다.<br>
<br>
Unity 6 가 출시되면서 내부 컴파일 파이프라인 동작 방식이 변경되었는데,<br>
<br>
이 변경 사항을 분석하고 [PR #701](https://github.com/rlabrecque/Steamworks.NET/pull/701) 을 통해 호환성 개선에 기여하게 되었다.<br>
<br>
이 과정에서 `delayCall` 의 중요성을 깊이 이해하게 되었고, 그 경험을 공유하고자 한다.<br>
<br>

### Unity 6 의 컴파일 파이프라인 변경 사항 분석
Unity 6 에서는 스크립트 리로드와 정의 기호 변경이 컴파일 파이프라인에 더 밀접하게 통합되었다.<br>
<br>
이전 버전에서는 정적 생성자에서 즉시 수행해도 괜찮았던 작업들이,<br>
<br>
새로운 파이프라인에서는 타이밍 조정이 필요하게 된 것이다.<br>
<br>
Steamworks.NET 의 `RedistInstall.cs` 코드를 분석해보니, `[InitializeOnLoad]` 정적 생성자에서 다음 작업들을 즉시 수행하고 있었다.<br>
<br>

```c#
[InitializeOnLoad]
public class RedistInstall
{
    static RedistInstall()
    {
        // 1. steam_appid.txt 파일 생성
        WriteSteamAppIdTxtFile();

        // 2. 스크립팅 정의 기호 추가
        AddDefineSymbols();  // STEAMWORKS_NET 정의

        // 3. 구형 DLL 감지
        CheckForOldDlls();
    }
}
```
<br>

Unity 6 의 변경된 컴파일 파이프라인에서는, 정적 생성자 실행 시점에<br>
<br>
스크립팅 정의 기호를 변경하면 컴파일이 다시 트리거될 수 있었다.<br>
<br>

```
Unity 6 에서의 동작 흐름을 추적한 결과:
1. 스크립트 컴파일 완료
2. 도메인 리로드 시작
3. 정적 생성자 실행 → 정의 기호 변경 감지
4. 컴파일 파이프라인이 변경을 감지하고 재컴파일 예약
5. 도메인 리로드 완료
6. 재컴파일 시작 → 2번으로 돌아감
```
<br>

### 해결 과정
문제의 근본 원인을 파악한 후, `delayCall` 을 사용하여 도메인 리로드가 완전히 완료된 후에 작업을 수행하도록 수정했다.<br>
<br>

```c#
[InitializeOnLoad]
public class RedistInstall
{
    static RedistInstall()
    {
        // delayCall 을 사용하여 안정된 시점에 실행
        EditorApplication.delayCall += () => {
            WriteSteamAppIdTxtFile();
            AddDefineSymbols();
            CheckForOldDlls();
        };
    }
}
```
<br>

이 수정으로 인해 다음과 같은 결과를 얻을 수 있었다.<br>
<br>
- 도메인 리로드가 완전히 완료된 후 작업 실행
- 컴파일 파이프라인이 안정된 상태에서 정의 기호 변경
- Unity 2017.1 부터 Unity 6 까지 모든 버전에서 안정적으로 동작
<br>

이 경험을 통해 Unity 버전 업그레이드 시 에디터 스크립트의 타이밍에 대한 재검토가 필요할 수 있다는 점,<br>
<br>
그리고 `delayCall` 이 이러한 호환성 이슈를 해결하는 데 효과적인 도구라는 점을 배울 수 있었다.<br>
<br><br>

## 에디터 도구 개발에서의 활용: soobak-asset-insights

Steamworks.NET 기여 경험 이후, 직접 개발한 에디터 도구에서도 `delayCall` 패턴을 적극 활용하게 되었다.<br>
<br>
[soobak-asset-insights](https://github.com/soo-bak/soobak-asset-insights) 는 Unity 프로젝트의 에셋 의존성을 분석하고<br>
<br>
빌드 크기 최적화를 돕기 위해 개발한 에디터 확장 도구이다.<br>
<br>

### 도구 개발 배경
프로젝트 규모가 커지면서 "이 에셋이 왜 빌드에 포함되는지", "어떤 에셋이 용량을 많이 차지하는지" 파악하기 어려워졌다.<br>
<br>
이를 해결하기 위해 의존성 그래프를 시각화하고, 최적화 포인트를 자동으로 찾아주는 도구를 만들게 되었다.<br>
<br>

### 주요 기능
- 에셋 의존성 경로 추적 및 시각화
- 빌드에 포함된 큰 에셋 식별
- 미사용 에셋 감지 및 일괄 삭제
- 순환 의존성 탐지
- 마크다운/JSON 형식의 리포트 생성
<br>

### 아키텍처 설계
```
Editor/
├── Core/
│   ├── Models/          - 데이터 모델
│   ├── Graph/           - 의존성 그래프
│   └── PathFinder/      - 경로 탐색 알고리즘
├── Services/
│   ├── IDependencyScanner  - 스캐너 인터페이스
│   └── IReportExporter     - 리포트 익스포터 인터페이스
└── UI/
    ├── EditorWindow/    - 메인 윈도우
    └── ContextMenu/     - 컨텍스트 메뉴 확장
```
<br>

### 초기화 전략에서 delayCall 활용
대규모 프로젝트에서 에셋 스캐닝은 수 초에서 수십 초가 걸릴 수 있는 작업이다.<br>
<br>
Steamworks.NET 에서의 경험을 바탕으로, 에디터 시작 시 자동으로 스캔을 수행하되<br>
<br>
에디터의 응답성을 해치지 않도록 다음과 같은 전략을 설계했다.<br>
<br>

```c#
[InitializeOnLoad]
public class AssetInsightsInitializer
{
    static AssetInsightsInitializer()
    {
        // 1단계: 에디터가 완전히 로드된 후 초기화 시작
        EditorApplication.delayCall += OnEditorReady;
    }

    static void OnEditorReady()
    {
        // 2단계: 캐시 확인 및 로드
        if (AssetInsightsCache.Exists() && !AssetInsightsCache.IsStale())
        {
            AssetInsightsCache.LoadAsync(OnCacheLoaded);
            return;
        }

        // 3단계: 캐시가 없거나 오래된 경우, 백그라운드 스캔 예약
        EditorApplication.delayCall += ScheduleBackgroundScan;
    }

    static void ScheduleBackgroundScan()
    {
        // Editor Coroutines 를 사용한 비동기 스캔
        EditorCoroutineUtility.StartCoroutineOwnerless(
            ScanAssetsAsync()
        );
    }

    static IEnumerator ScanAssetsAsync()
    {
        var allAssets = AssetDatabase.GetAllAssetPaths();
        int processedCount = 0;

        foreach (var assetPath in allAssets)
        {
            ProcessAsset(assetPath);
            processedCount++;

            // 100개마다 한 프레임 양보하여 에디터 응답성 유지
            if (processedCount % 100 == 0)
            {
                EditorUtility.DisplayProgressBar(
                    "Asset Insights",
                    $"Scanning... {processedCount}/{allAssets.Length}",
                    (float)processedCount / allAssets.Length
                );
                yield return null;
            }
        }

        EditorUtility.ClearProgressBar();
        AssetInsightsCache.Save();
    }
}
```
<br>

### delayCall 체이닝을 통한 단계별 초기화
여러 단계의 초기화가 필요한 경우, `delayCall` 을 체이닝하여 각 단계 사이에 에디터가 안정화될 시간을 확보했다.<br>
<br>

```c#
static void InitializeWithChaining()
{
    EditorApplication.delayCall += () => {
        // 1단계: 설정 로드
        LoadSettings();

        EditorApplication.delayCall += () => {
            // 2단계: 캐시 초기화
            InitializeCache();

            EditorApplication.delayCall += () => {
                // 3단계: UI 준비
                PrepareUI();
            };
        };
    };
}
```
<br>

이 패턴의 장점은 각 단계가 독립적으로 실행되어,<br>
<br>
하나의 단계에서 발생한 예외가 다른 단계에 영향을 주지 않는다는 것이다.<br>
<br>
실제로 이 도구를 사용하면서 에디터 시작 시 불필요한 지연 없이,<br>
<br>
도메인 리로드 중 충돌도 방지하면서 안정적으로 초기화가 완료되는 것을 확인할 수 있었다.<br>
<br><br>

## 고급 활용: delayCall 과 다른 에디터 API 조합

### AssetDatabase 작업과의 조합
에셋을 생성하거나 수정한 후, 관련 작업을 수행해야 할 때 `delayCall` 이 유용하다.<br>
<br>

```c#
public static void CreateAndConfigureAsset()
{
    // 1. 에셋 생성
    var asset = ScriptableObject.CreateInstance<MyConfig>();
    AssetDatabase.CreateAsset(asset, "Assets/MyConfig.asset");

    // 2. AssetDatabase 가 갱신될 때까지 대기 후 추가 작업
    EditorApplication.delayCall += () => {
        // 이 시점에서 에셋이 완전히 저장되어 있음
        var loadedAsset = AssetDatabase.LoadAssetAtPath<MyConfig>(
            "Assets/MyConfig.asset"
        );
        ConfigureAsset(loadedAsset);
        EditorUtility.SetDirty(loadedAsset);
        AssetDatabase.SaveAssets();
    };
}
```
<br>

### Selection 변경과의 조합
에디터에서 선택된 오브젝트가 변경될 때, 즉시 반응하면 타이밍 이슈가 생길 수 있다.<br>
<br>

```c#
[InitializeOnLoad]
public class SelectionWatcher
{
    static SelectionWatcher()
    {
        Selection.selectionChanged += OnSelectionChanged;
    }

    static void OnSelectionChanged()
    {
        // 선택 변경 직후가 아닌, 안정된 시점에 처리
        EditorApplication.delayCall += ProcessSelection;
    }

    static void ProcessSelection()
    {
        var selected = Selection.activeObject;
        if (selected != null)
        {
            AnalyzeObject(selected);
        }
    }
}
```
<br><br>

## delayCall vs EditorCoroutine vs update: 상세 비교

각각의 메커니즘은 서로 다른 목적에 최적화되어 있다.<br>
<br>

### EditorApplication.delayCall
```c#
EditorApplication.delayCall += () => {
    // 다음 에디터 업데이트에서 한 번 실행
};
```
<br>

<b>특징:</b>
- 일회성 실행
- 등록 순서대로 실행 (FIFO)
- 도메인 리로드 시 등록된 콜백 소멸
- 메모리 오버헤드가 적음
<br>

<b>적합한 사용:</b>
- 초기화 지연
- 일회성 후처리 작업
- 에디터 상태 안정화 대기
<br><br>

### EditorApplication.update
```c#
void OnEnable()
{
    EditorApplication.update += OnUpdate;
}

void OnDisable()
{
    EditorApplication.update -= OnUpdate;
}

void OnUpdate()
{
    // 매 에디터 프레임마다 실행
}
```
<br>

<b>특징:</b>
- 매 프레임 반복 실행
- 명시적으로 해제해야 함
- 도메인 리로드 시 재등록 필요
- 지속적인 CPU 사용
<br>

<b>적합한 사용:</b>
- 실시간 모니터링
- 지속적인 상태 확인
- 에디터 내 애니메이션
<br><br>

### Editor Coroutines
```c#
IEnumerator MyCoroutine()
{
    yield return null;  // 다음 에디터 프레임
    yield return new EditorWaitForSeconds(1f);  // 1초 대기 (에디터 시간 기준)
}

// 실행
EditorCoroutineUtility.StartCoroutine(MyCoroutine(), this);
```
<br>

> Editor Coroutines 패키지는 `EditorWaitForSeconds` 등 에디터 전용 yield instruction 을 제공한다.<br>
> 런타임의 `WaitForSeconds`, `WaitUntil` 등과는 다르므로 패키지 문서를 확인하는 것이 좋다.<br>
<br>

<b>특징:</b>
- 런타임 코루틴과 유사한 문법
- 복잡한 비동기 흐름 표현 가능
- 진행 상태 추적 용이
- Unity.EditorCoroutines 패키지 필요
<br>

<b>적합한 사용:</b>
- 장시간 작업 (스캐닝, 빌드 등)
- 진행률 표시가 필요한 작업
- 여러 단계로 나뉜 순차 작업
<br><br>

## 주의사항과 디버깅

### 흔한 실수
<b>1. 무한 delayCall 등록</b>
```c#
// 잘못된 예
EditorApplication.delayCall += () => {
    DoSomething();
    EditorApplication.delayCall += SameCallback;  // 무한 루프!
};

// 올바른 예
void ConditionalDelayCall()
{
    if (needsMoreWork)
    {
        EditorApplication.delayCall += ConditionalDelayCall;
    }
}
```
<br>

<b>2. 도메인 리로드 후 상태 손실</b>
```c#
// 문제: 도메인 리로드 시 data 가 null 이 됨
static MyData data;

static MyClass()
{
    EditorApplication.delayCall += () => {
        data = LoadData();  // 이 시점에 로드해도
    };
}

void SomeMethod()
{
    data.DoSomething();  // 도메인 리로드 직후에는 null!
}
```
<br>

<b>3. 플레이 모드 전환 시 타이밍</b>
```c#
// 플레이 모드 진입 시 delayCall 이 실행되지 않을 수 있음
[InitializeOnLoad]
static class PlayModeHandler
{
    static PlayModeHandler()
    {
        EditorApplication.playModeStateChanged += OnPlayModeChanged;
    }

    static void OnPlayModeChanged(PlayModeStateChange state)
    {
        if (state == PlayModeStateChange.EnteredEditMode)
        {
            // 플레이 모드 종료 후 안전하게 작업 수행
            EditorApplication.delayCall += PostPlayModeCleanup;
        }
    }
}
```
<br>

### 디버깅 팁
```c#
// delayCall 실행 순서 추적
static int callOrder = 0;

static void TrackDelayCall(string name)
{
    int myOrder = callOrder++;
    double registeredTime = EditorApplication.timeSinceStartup;
    EditorApplication.delayCall += () => {
        double executedTime = EditorApplication.timeSinceStartup;
        Debug.Log($"[{myOrder}] {name} - 등록: {registeredTime:F3}s, 실행: {executedTime:F3}s");
    };
}
```
<br>

에디터 환경에서는 `Time.frameCount` 가 플레이 모드가 아닐 때 항상 0 이므로,<br>
<br>
`EditorApplication.timeSinceStartup` 을 사용하는 것이 더 유용하다.<br>
<br><br>

## 결론

`EditorApplication.delayCall` 은 단순해 보이지만, Unity 에디터의 라이프사이클을 이해하고 안정적인 에디터 확장을 만드는 데 핵심적인 역할을 한다.<br>
<br>

핵심 내용들을 정리하면 다음과 같다.<br>
<br>
- `delayCall` 은 에디터가 안정된 상태에서 코드를 실행하도록 보장한다.
- `[InitializeOnLoad]` 정적 생성자에서 에디터 상태를 변경하는 작업은 `delayCall` 로 감싸는 것이 안전하다.
- Unity 버전 업그레이드 시 컴파일 파이프라인 동작이 변경될 수 있으므로, 타이밍에 민감한 코드는 재검토가 필요하다.
- `delayCall`, `update`, `EditorCoroutine` 은 각각 다른 목적에 최적화되어 있으므로, 상황에 맞게 선택해야 한다.
<br>

에디터 도구를 개발할 때 "지금 당장" 실행해야 하는지, "안전한 시점"에 실행해야 하는지를 항상 고민해보는 것이 좋다.<br>
<br>
"안전한 시점"에 실행해야 하는 작업이라면 `delayCall` 을 활용하는 것을 권장한다.<br>
<br>

---

### 참고 자료
- [Unity 공식 문서 - EditorApplication.delayCall](https://docs.unity3d.com/ScriptReference/EditorApplication-delayCall.html)
- [Unity 공식 문서 - Order of Execution](https://docs.unity3d.com/Manual/ExecutionOrder.html)
- [Steamworks.NET - Unity 6 호환성 개선 PR](https://github.com/rlabrecque/Steamworks.NET/pull/701)
- [soobak-asset-insights](https://github.com/soo-bak/soobak-asset-insights)
- [Unity 코루틴(Coroutine) 분석](https://soo-bak.github.io/dev/unity/UnityCoroutine/)