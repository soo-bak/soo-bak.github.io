---
layout: single
title: "Unity 에셋 시스템 (3) - Scene Management - soo:bak"
date: "2026-03-05 23:09:00 +0900"
description: 씬 구조, 동기·비동기 씬 로딩, Additive 씬, DontDestroyOnLoad, 씬 언로딩과 메모리 해제를 설명합니다.
tags:
  - Unity
  - 에셋
  - Scene
  - 씬관리
  - 모바일
---

## 에셋에서 씬으로

[Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)에서는 에셋 하나가 디스크와 메모리 사이를 오가는 과정을 다루었습니다. 에셋은 직렬화를 거쳐 파일로 저장되고 역직렬화를 거쳐 메모리로 복원되며, `Instantiate`는 GameObject와 컴포넌트만 복제하고 Mesh와 Texture 같은 공유 에셋은 참조만 복사합니다. 빌드 크기를 키우고 메모리 관리를 어렵게 하는 Resources 폴더의 구조적 한계도 함께 살펴보았습니다.

그런데 실행 중인 게임이 다루는 단위는 에셋 하나가 아니라 화면 하나입니다. 새 화면이 나타나려면 그 화면에 필요한 수많은 GameObject와 이들이 참조하는 에셋이 한꺼번에 준비되어야 합니다. 이 GameObject들과 참조 에셋이 모여 이루는 실행 단위가 **씬(Scene)**입니다.

메뉴에서 게임 플레이로, 다시 결과 화면으로 넘어가는 게임 흐름의 전환은 결국 씬 하나를 언로드하고 다른 씬을 로드하는 작업입니다. 이 교체 한 번에 이전 씬의 오브젝트 정리와 새 씬의 에셋 로드가 함께 일어나고, 메모리 사용량이 수십~수백 MB 변동할 수 있습니다. 씬을 어떻게 나누고 전환을 언제 어떤 방식으로 처리하느냐에 따라, 로딩 중 화면이 멈추기도 하고 두 씬의 에셋이 겹치는 구간에는 메모리 피크가 생기기도 합니다.

이 글에서는 씬의 구조에서 시작해 동기·비동기 씬 로딩, 여러 씬을 함께 올리는 Additive 모드, 씬 전환에도 오브젝트를 유지하는 DontDestroyOnLoad, 씬 언로딩과 메모리 해제, 대규모 월드를 위한 씬 분할 전략까지 차례로 살펴봅니다.

---

## 씬(Scene)의 구조

씬 하나는 화면을 구성하는 GameObject들의 모음입니다. 카메라와 조명, 캐릭터와 배경, UI처럼 역할이 다른 오브젝트가 한 씬 안에 함께 놓입니다. 각 GameObject에는 위치와 회전을 나타내는 Transform, 형상을 화면에 그리는 Renderer, 충돌을 판정하는 Collider, 동작을 정의하는 스크립트 같은 컴포넌트가 담기고, 이 가운데 일부는 머티리얼, 텍스처, 메쉬 같은 외부 에셋을 참조합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 전체 씬 컨테이너 -->
  <rect x="10" y="10" width="500" height="500" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 (.unity 파일)</text>

  <!-- Main Camera -->
  <rect x="30" y="52" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="72" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Camera (GameObject)</text>
  <text x="56" y="90" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="106" font-family="sans-serif" font-size="11" fill="currentColor">Camera</text>
  <text x="56" y="118" font-family="sans-serif" font-size="11" fill="currentColor">AudioListener</text>

  <!-- Directional Light -->
  <rect x="30" y="134" width="460" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="154" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Directional Light (GameObject)</text>
  <text x="56" y="172" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="184" font-family="sans-serif" font-size="11" fill="currentColor">Light</text>

  <!-- Player -->
  <rect x="30" y="200" width="460" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="220" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Player (GameObject)</text>
  <text x="56" y="238" font-family="sans-serif" font-size="11" fill="currentColor">Transform</text>
  <text x="56" y="254" font-family="sans-serif" font-size="11" fill="currentColor">MeshRenderer</text>
  <!-- 참조 화살표: MeshRenderer → Material → Texture -->
  <line x1="144" y1="251" x2="164" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="164,248 170,251 164,254" fill="currentColor"/>
  <text x="174" y="254" font-family="sans-serif" font-size="11" fill="currentColor">Material</text>
  <line x1="222" y1="251" x2="242" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="242,248 248,251 242,254" fill="currentColor"/>
  <text x="252" y="254" font-family="sans-serif" font-size="11" fill="currentColor">Texture</text>
  <text x="56" y="270" font-family="sans-serif" font-size="11" fill="currentColor">Rigidbody</text>
  <text x="56" y="284" font-family="sans-serif" font-size="11" fill="currentColor">PlayerController (스크립트)</text>

  <!-- Environment -->
  <rect x="30" y="300" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="320" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Environment (GameObject)</text>
  <text x="56" y="338" font-family="sans-serif" font-size="11" fill="currentColor">Ground</text>
  <text x="56" y="354" font-family="sans-serif" font-size="11" fill="currentColor">Building_01</text>
  <text x="56" y="366" font-family="sans-serif" font-size="11" fill="currentColor">Building_02</text>

  <!-- Canvas (UI) -->
  <rect x="30" y="382" width="460" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="402" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Canvas (UI)</text>
  <text x="56" y="420" font-family="sans-serif" font-size="11" fill="currentColor">HealthBar</text>
  <text x="56" y="432" font-family="sans-serif" font-size="11" fill="currentColor">ScoreText</text>

  <!-- 보조 설명 -->
  <text x="260" y="468" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">각 GameObject 안에 컴포넌트들이 포함됨</text>
  <text x="260" y="484" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">MeshRenderer → Material → Texture 는 에셋 참조 관계</text>
</svg>
</div>

그림에서 보듯 씬 파일에는 GameObject와 컴포넌트의 구성만 들어 있는 것이 아니라, 각 컴포넌트가 어떤 외부 에셋을 참조하는지도 함께 기록됩니다. Player의 MeshRenderer가 Material을 참조하고 그 Material이 다시 Texture를 참조하는 연결 관계까지 씬 파일 안에 담깁니다.

씬을 저장하면 이 구성 전체가 직렬화되어 `.unity` 파일에 기록되고, 각 오브젝트는 fileID라는 고유 번호로 식별됩니다. 씬을 로드할 때는 반대로 Unity가 이 데이터를 역직렬화해 메모리 위의 오브젝트로 복원합니다.

> 에셋이 YAML로 직렬화되어 디스크에 기록되는 과정은 [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)에서 자세히 다룹니다.

### Build Settings에 씬 등록

씬을 만들었다고 해서 자동으로 빌드에 포함되지는 않습니다. 기본 씬 로딩 방식으로 사용할 씬은 **Build Settings**(File → Build Settings)의 **Scenes In Build** 목록에 직접 등록해야 합니다. 목록에 오른 씬은 위에서부터 차례로 인덱스 번호를 받고, 그중 0번 씬이 앱을 실행할 때 가장 먼저 로드됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 외곽 컨테이너 -->
  <rect x="10" y="10" width="500" height="260" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Build Settings의 씬 목록</text>

  <!-- Scenes In Build 라벨 -->
  <text x="30" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Scenes In Build:</text>

  <!-- 테이블 외곽 -->
  <rect x="30" y="68" width="340" height="120" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
  <!-- 인덱스 칼럼 구분선 -->
  <line x1="72" y1="68" x2="72" y2="188" stroke="currentColor" stroke-width="1"/>
  <!-- 행 구분선 -->
  <line x1="30" y1="98" x2="370" y2="98" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="30" y1="128" x2="370" y2="128" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="30" y1="158" x2="370" y2="158" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Row 0 (하이라이트) -->
  <rect x="31" y="69" width="338" height="29" fill="currentColor" fill-opacity="0.06"/>
  <text x="51" y="88" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="currentColor">0</text>
  <text x="82" y="88" font-family="monospace" font-size="11" fill="currentColor">Scenes/Loading.unity</text>
  <text x="380" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">← 앱 시작 시 로드</text>

  <!-- Row 1 -->
  <text x="51" y="118" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">1</text>
  <text x="82" y="118" font-family="monospace" font-size="11" fill="currentColor">Scenes/MainMenu.unity</text>

  <!-- Row 2 -->
  <text x="51" y="148" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">2</text>
  <text x="82" y="148" font-family="monospace" font-size="11" fill="currentColor">Scenes/GamePlay.unity</text>

  <!-- Row 3 -->
  <text x="51" y="178" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">3</text>
  <text x="82" y="178" font-family="monospace" font-size="11" fill="currentColor">Scenes/Result.unity</text>

  <!-- 결론 라인 -->
  <text x="30" y="216" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 인덱스 0번이 첫 실행 씬</text>
  <text x="30" y="234" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 목록에 없는 씬은 빌드에 포함되지 않음</text>
  <text x="30" y="252" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 씬 이름 또는 인덱스로 런타임 로딩 가능</text>
</svg>
</div>

<br>

이 목록을 기준으로 씬을 불러오는 것이 `SceneManager`입니다. 목록에 등록된 씬은 런타임에서 이름이나 인덱스로 지정해 불러올 수 있고, 목록에 없는 씬은 일반 빌드에 포함되지 않아 이 방식으로는 찾을 수 없습니다.

등록하지 않은 씬까지 런타임에 로드해야 한다면 Unity의 **Addressables** 시스템이 필요하지만, 이는 별도의 패키징과 로딩 규칙을 따르는 다른 주제입니다. 이 글에서는 등록된 씬을 `SceneManager`로 불러오는 기본 흐름을 다룹니다. 그 첫 방식이 다음 절에서 살펴볼 동기 로딩입니다.

---

## SceneManager.LoadScene: 동기 로딩

씬을 불러오는 가장 단순한 API가 `SceneManager.LoadScene`입니다. 이 API는 씬을 **동기적(Synchronous)**으로 로드하지만, 동기라고 해서 호출한 줄이 그 자리에서 멈추지는 않습니다. 호출은 같은 프레임 안에서 곧바로 반환되어 뒤따르는 코드도 계속 실행되고, 실제 씬 교체는 다음 프레임에 이루어집니다.

실제 비용은 다음 프레임에서 나타납니다. Unity가 새 씬의 오브젝트와 에셋을 로드하고 활성화하는 동안 메인 스레드는 이 작업을 우선 처리해야 합니다. Unity의 게임 로직 실행, 입력 처리, 렌더링 명령 생성도 같은 메인 스레드에서 이루어지므로, 동기 로딩이 진행되는 동안에는 다음 화면을 그리거나 입력에 반응할 시간이 생기지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">동기 로딩의 실행 흐름</text>

  <!-- 프레임 N 영역 -->
  <rect x="10" y="36" width="540" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="24" y="56" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임 N</text>

  <!-- 호출 시점 -->
  <rect x="30" y="66" width="500" height="54" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">호출 시점</text>
  <text x="44" y="100" font-family="sans-serif" font-size="11" fill="currentColor">SceneManager.LoadScene("GamePlay") 호출</text>
  <text x="44" y="114" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">호출 이후 같은 프레임 내 나머지 코드는 계속 실행됨</text>

  <!-- 세로 화살표: 프레임 N → 다음 프레임 블로킹 -->
  <line x1="280" y1="126" x2="280" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,140 280,147 283,140" fill="currentColor"/>

  <!-- 다음 프레임 (블로킹 구간) -->
  <rect x="30" y="150" width="500" height="254" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="44" y="170" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">다음 프레임 (메인 스레드 블로킹, 로딩 완료까지)</text>

  <!-- 6단계 -->
  <rect x="50" y="182" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="200" font-family="sans-serif" font-size="11" fill="currentColor">1. 현재 씬의 모든 오브젝트 파괴 (OnDisable → OnDestroy)</text>

  <line x1="280" y1="210" x2="280" y2="218" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,218 280,222 282,218" fill="currentColor"/>

  <rect x="50" y="224" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="242" font-family="sans-serif" font-size="11" fill="currentColor">2. 새 씬 파일 읽기 (디스크 I/O)</text>

  <line x1="280" y1="252" x2="280" y2="260" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,260 280,264 282,260" fill="currentColor"/>

  <rect x="50" y="266" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="284" font-family="sans-serif" font-size="11" fill="currentColor">3. 참조 에셋 로딩 (텍스처, 메쉬, 오디오 등)</text>

  <line x1="280" y1="294" x2="280" y2="302" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,302 280,306 282,302" fill="currentColor"/>

  <rect x="50" y="308" width="460" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="326" font-family="sans-serif" font-size="11" fill="currentColor">4. 모든 오브젝트 역직렬화 (메모리 배치)</text>

  <line x1="280" y1="336" x2="280" y2="344" stroke="currentColor" stroke-width="1"/>
  <polygon points="278,344 280,348 282,344" fill="currentColor"/>

  <rect x="50" y="350" width="220" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="64" y="368" font-family="sans-serif" font-size="11" fill="currentColor">5. Awake() 호출</text>

  <rect x="290" y="350" width="220" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="304" y="368" font-family="sans-serif" font-size="11" fill="currentColor">6. OnEnable() 호출</text>

  <text x="530" y="400" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">화면 갱신 없음 (게임 멈춤)</text>

  <!-- 세로 화살표: 프레임 N → N+1 -->
  <line x1="280" y1="416" x2="280" y2="432" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,432 280,439 283,432" fill="currentColor"/>

  <!-- 로딩 완료 후 첫 프레임 -->
  <rect x="10" y="442" width="540" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="24" y="462" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">로딩 완료 후 첫 프레임</text>
  <text x="44" y="480" font-family="sans-serif" font-size="11" fill="currentColor">Start() 호출 (첫 Update() 직전)</text>
  <text x="44" y="494" font-family="sans-serif" font-size="11" fill="currentColor">새 씬의 첫 Update() 실행</text>

  <!-- 보조 텍스트 -->
  <text x="280" y="524" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">실제 씬 전환은 다음 프레임에서 수행 · 로딩 완료까지 메인 스레드 블로킹 · 화면 갱신 없음</text>
</svg>
</div>

블로킹 시간은 새 씬에서 생성해야 하는 오브젝트 수와, 그 오브젝트들이 참조하는 에셋의 양에 따라 길어집니다. 텍스처, 메쉬, 오디오처럼 로드해야 할 데이터가 많은 게임 씬에서는 메인 스레드가 몇 초 동안 로딩 작업을 처리할 수 있습니다. 이 동안 화면 갱신과 입력 처리가 멈추므로, 사용자는 앱이 응답하지 않는 상태로 인식할 수 있습니다. 모바일 환경에서는 이런 정지가 길어지면 OS가 앱을 응답 없음 상태로 판단해 종료할 가능성도 있습니다.

그래서 동기 로딩은 짧은 정지가 허용되는 상황에 한정해서 사용하는 편이 좋습니다. 예를 들어 앱 시작 시 첫 씬을 불러오면서 스플래시 화면이 표시되는 구간이나, 포함된 오브젝트와 에셋이 적어 로딩이 거의 즉시 끝나는 작은 씬이 이에 해당합니다. 플레이 중에 큰 게임 씬으로 전환해야 한다면, 다음 절에서 다룰 비동기 로딩을 사용하는 편이 적절합니다.

### 기존 씬의 처리

동기 로딩에서 새 씬을 불러올 때 기본 모드는 `LoadSceneMode.Single`입니다. 이 모드에서는 새 씬이 현재 씬을 대체하므로, Unity는 기존 씬의 GameObject들을 먼저 정리합니다. 각 오브젝트는 비활성화 과정에서 `OnDisable`을 받고, 이어서 파괴 과정에서 `OnDestroy`를 받습니다. 구독 해제나 임시 상태 정리처럼 오브젝트 수명에 묶인 작업은 이 시점에 처리해야 합니다.

다만 GameObject가 파괴되었다고 해서 그 오브젝트가 참조하던 텍스처, 메쉬, 오디오 같은 에셋까지 즉시 메모리에서 내려가는 것은 아닙니다. 오브젝트의 수명과 에셋 메모리의 수명은 별도로 관리됩니다. Unity는 새 씬 로딩이 끝난 뒤 `Resources.UnloadUnusedAssets()`를 자동으로 실행하고, 그때 더 이상 참조되지 않는 에셋을 해제합니다.

이 순서 때문에 씬 전환 중에는 메모리 피크가 생길 수 있습니다. 이전 씬의 에셋이 아직 해제되지 않은 상태에서 새 씬의 에셋이 먼저 로드되기 때문입니다. 잠시 동안 두 씬의 에셋이 함께 메모리에 올라와 있고, 전환이 끝난 뒤 사용되지 않는 에셋을 정리하면서 메모리가 내려갑니다. 큰 씬끼리 바로 전환할 때 이 구간이 모바일 메모리 한계를 넘기 쉬운 지점입니다.

---

## SceneManager.LoadSceneAsync: 비동기 로딩

앞 절에서 본 프레임 정지는 씬 로딩이 한 프레임에 몰리기 때문에 생깁니다. 이 멈춤을 줄이려면 무거운 작업을 여러 프레임에 나누어 처리하면서도, 그동안 게임 루프가 계속 진행되도록 해야 합니다. `SceneManager.LoadSceneAsync`는 씬을 **비동기적(Asynchronous)**으로 로드해 바로 이 방식을 따릅니다.

비동기 로딩은 이 작업을 성격에 따라 둘로 나눕니다. 시간이 오래 걸리는 파일 읽기(I/O)와 역직렬화는 백그라운드 스레드에서 이루어지고, 읽어 들인 오브젝트를 실제 씬에 연결하는 통합(Integration) 작업만 메인 스레드가 여러 프레임에 걸쳐 조금씩 처리합니다. 메인 스레드가 한 프레임에 감당할 양이 줄어든 덕분에, 로딩이 진행되는 동안에도 화면이 갱신되고 입력도 처리됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">비동기 로딩의 실행 흐름</text>
  <line x1="90" y1="58" x2="590" y2="58" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="590,55 597,58 590,61" fill="currentColor"/>
  <text x="604" y="62" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">시간</text>
  <text x="110" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">N</text>
  <line x1="110" y1="54" x2="110" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+1</text>
  <line x1="190" y1="54" x2="190" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+2</text>
  <line x1="270" y1="54" x2="270" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="350" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+3</text>
  <line x1="350" y1="54" x2="350" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">N+K</text>
  <line x1="440" y1="54" x2="440" y2="62" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="50" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">N+K+1</text>
  <line x1="540" y1="54" x2="540" y2="62" stroke="currentColor" stroke-width="1"/>
  <line x1="390" y1="70" x2="390" y2="310" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.3"/>
  <text x="14" y="108" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">백그라운드</text>
  <text x="14" y="120" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드</text>
  <rect x="90" y="80" width="370" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">파일 I/O + 역직렬화</text>
  <text x="275" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">디스크 읽기, 에셋 데이터 역직렬화</text>
  <text x="14" y="170" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">메인</text>
  <text x="14" y="182" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드</text>
  <rect x="90" y="148" width="370" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">게임 실행 + 오브젝트 통합 처리</text>
  <text x="275" y="184" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">화면 갱신 유지, 매 프레임 분산 처리</text>
  <rect x="480" y="80" width="120" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="540" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 활성화</text>
  <text x="540" y="120" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Awake()</text>
  <text x="540" y="138" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">OnEnable()</text>
  <text x="540" y="156" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Start()</text>
  <text x="540" y="176" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">progress: 1.0</text>
  <line x1="460" y1="106" x2="476" y2="106" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="476,103 482,106 476,109" fill="currentColor"/>
  <line x1="460" y1="174" x2="476" y2="174" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="476,171 482,174 476,177" fill="currentColor"/>
  <text x="44" y="240" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">progress</text>
  <rect x="90" y="224" width="510" height="28" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <rect x="90" y="224" width="370" height="28" rx="5" fill="currentColor" fill-opacity="0.08"/>
  <text x="110" y="242" font-family="sans-serif" font-size="10" fill="currentColor">0.0</text>
  <text x="190" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.1</text>
  <text x="270" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.3</text>
  <text x="350" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">0.5</text>
  <text x="440" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">0.9</text>
  <text x="540" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1.0</text>
  <line x1="460" y1="224" x2="460" y2="252" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <rect x="90" y="272" width="370" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="275" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">에셋 로딩 구간 (0.0 ~ 0.9)</text>
  <rect x="480" y="272" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="540" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">활성화 (0.9 ~ 1.0)</text>
  <text x="310" y="326" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">백그라운드 스레드: I/O와 역직렬화 담당</text>
  <text x="310" y="342" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메인 스레드: 게임 실행 유지 + 오브젝트 통합 담당</text>
  <text x="310" y="358" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로딩 중에도 화면 갱신과 입력 처리가 계속됨</text>
</svg>
</div>

### AsyncOperation과 progress

`LoadSceneAsync`는 호출 직후 **AsyncOperation** 객체를 반환합니다. 이 객체에는 비동기 로딩 작업의 상태가 들어 있으며, `progress` 프로퍼티로 현재 진행 정도를 확인할 수 있습니다. 값의 범위는 0.0부터 1.0까지지만, 씬 로딩에서는 이 값을 그대로 로딩 바의 0%부터 100%까지로 해석하면 실제 흐름과 어긋날 수 있습니다.

씬 데이터 읽기, 역직렬화, 메모리 배치처럼 전환 전에 준비해야 하는 작업은 주로 `progress` 0.0부터 0.9까지의 구간에 반영됩니다. `progress`가 `0.9f`에 도달했다는 것은 새 씬을 활성화하기 직전까지의 준비가 끝났다는 뜻에 가깝습니다.

남은 0.9에서 1.0까지의 구간은 씬 활성화 단계입니다. 이때 준비된 오브젝트가 실제 씬으로 전환되고, 활성화 과정에서 필요한 초기화가 이어집니다. 따라서 로딩 화면의 진행 바를 표시할 때는 보통 `operation.progress / 0.9f`로 0.0부터 0.9까지의 구간을 0%부터 100%까지로 환산하고, 활성화 시점은 다음 절의 `allowSceneActivation`으로 따로 다룹니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">progress 값의 의미</text>
  <!-- 진행 바 전체 -->
  <rect x="30" y="38" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <!-- 에셋 로딩 구간 (0.0 ~ 0.9) -->
  <rect x="30" y="38" width="384" height="50" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="222" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋 로딩 구간</text>
  <text x="222" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">디스크 읽기 · 역직렬화 · 메모리 배치</text>
  <!-- 활성화 구간 (0.9 ~ 1.0) -->
  <rect x="414" y="38" width="96" height="50" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="462" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활성화</text>
  <text x="462" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Awake · Start</text>
  <!-- 눈금 레이블 -->
  <text x="30" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">0.0</text>
  <line x1="30" y1="88" x2="30" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <text x="414" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">0.9</text>
  <line x1="414" y1="88" x2="414" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <text x="510" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1.0</text>
  <line x1="510" y1="88" x2="510" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <!-- 구분선 0.9 -->
  <line x1="414" y1="38" x2="414" y2="88" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <!-- 하단: 로딩 바 환산 공식 -->
  <rect x="100" y="128" width="340" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">로딩 바 표시 비율 = operation.progress / 0.9f</text>
  <text x="270" y="160" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">0.9 이전까지를 100%로 환산</text>
  <!-- 화살표: 0.0~0.9 구간 → 공식 -->
  <line x1="222" y1="88" x2="222" y2="124" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <polygon points="219,124 222,130 225,124" fill="currentColor"/>
  <!-- 보조 설명 -->
  <text x="270" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">progress가 0.9에 도달하면 에셋 로딩 완료, 이후 씬 활성화 단계 진입</text>
</svg>
</div>

### allowSceneActivation으로 활성화 시점 제어

`progress`가 `0.9f`에 도달했다는 것은 전환에 필요한 준비가 끝나고, 이제 씬을 활성화할 수 있는 상태에 가까워졌다는 뜻입니다. 이 지점에서 곧바로 새 씬으로 넘어가도 되지만, 로딩 화면의 페이드 아웃을 끝내거나 "터치하여 시작" 입력을 기다려야 하는 경우도 있습니다.

이때 사용하는 스위치가 `AsyncOperation.allowSceneActivation`입니다. 로딩을 시작한 뒤 이 값을 `false`로 두면, 작업은 `progress` `0.9f`에서 대기하고 새 씬은 아직 활성화되지 않습니다. 전환 연출이나 사용자 입력까지 마쳤다면 값을 `true`로 바꿉니다. 그때 남아 있던 활성화 단계가 진행되고, 새 씬의 오브젝트가 실제 실행 상태로 들어오며 생명주기 콜백이 이어집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 외곽 컨테이너 -->
  <rect x="10" y="10" width="500" height="370" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">allowSceneActivation 활용</text>

  <!-- Phase 1: 로딩 시작 -->
  <rect x="30" y="48" width="460" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. 로딩 시작</text>
  <text x="44" y="82" font-family="monospace" font-size="10" fill="currentColor">AsyncOperation op = SceneManager.LoadSceneAsync("GamePlay");</text>
  <text x="44" y="96" font-family="monospace" font-size="10" fill="currentColor">op.allowSceneActivation = false;</text>

  <!-- 화살표 1→2 -->
  <line x1="260" y1="106" x2="260" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,120 260,127 263,120" fill="currentColor"/>

  <!-- Phase 2: 대기 (점선) -->
  <rect x="30" y="130" width="460" height="58" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="44" y="148" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. 로딩 진행 (progress → 0.9)</text>
  <text x="44" y="166" font-family="sans-serif" font-size="11" fill="currentColor">씬 데이터는 메모리에 준비 완료</text>
  <text x="44" y="180" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">활성화되지 않음, 대기 상태</text>

  <!-- 화살표 2→3 -->
  <line x1="260" y1="188" x2="260" y2="202" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,202 260,209 263,202" fill="currentColor"/>

  <!-- Phase 3: 활성화 -->
  <rect x="30" y="212" width="460" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="44" y="230" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. 원하는 시점에 활성화</text>
  <text x="44" y="246" font-family="monospace" font-size="10" fill="currentColor">op.allowSceneActivation = true;</text>
  <text x="44" y="262" font-family="sans-serif" font-size="11" fill="currentColor">→ Awake, OnEnable, Start 호출</text>
  <text x="44" y="276" font-family="sans-serif" font-size="11" fill="currentColor">→ 씬 전환 완료</text>

  <!-- 활용 예 -->
  <line x1="30" y1="300" x2="490" y2="300" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="30" y="320" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활용 예:</text>
  <text x="44" y="338" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 로딩 화면의 "터치하여 시작" 연출</text>
  <text x="44" y="354" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 최소 로딩 시간 보장 (너무 빠르면 로딩 화면이 깜빡임)</text>
  <text x="44" y="370" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">• 다른 비동기 작업(네트워크 등)과 동기화</text>
</svg>
</div>

<br>

활성화를 보류한 상태에서는 완료를 판단하는 기준도 달라집니다. `allowSceneActivation`이 `false`이면 작업은 `progress` `0.9f`에서 대기하고, `AsyncOperation.isDone`은 아직 `true`가 되지 않습니다. 따라서 코루틴에서 `yield return operation`으로 완료를 기다리면, 활성화를 허용하기 전까지 코루틴도 그 지점에서 멈춰 있게 됩니다.

이 구간에서는 `isDone`을 준비 완료 신호로 쓰지 않습니다. 대신 `progress >= 0.9f`를 확인해 새 씬을 활성화할 준비가 되었는지 판단합니다. 이 시점에 로딩 화면의 시작 버튼을 표시하거나 페이드 아웃 같은 전환 연출을 마무리하고, 실제로 넘어가야 할 때 `allowSceneActivation`을 `true`로 바꾸면 됩니다. `isDone`은 씬 활성화까지 끝난 뒤에 확인할 최종 완료 신호로 보는 편이 맞습니다.

한 가지 더 주의할 점은 동기 로딩과 섞어 쓰는 경우입니다. `SceneManager.LoadScene`처럼 동기 씬 로딩을 호출하면, 대기 중이던 비동기 작업이 함께 진행되며 의도하지 않은 시점에 활성화될 수 있습니다. `allowSceneActivation`으로 전환 시점을 잡아 두었다면, 같은 흐름 안에서 별도의 동기 씬 로딩을 끼워 넣지 않는 편이 안전합니다.

### 비동기 로딩에도 남는 프레임 드롭

비동기 로딩을 사용해도 모든 비용이 백그라운드로 사라지는 것은 아닙니다. 디스크 읽기나 데이터 준비는 여러 프레임에 나뉘어 진행되지만, 준비된 에셋을 Unity 객체로 통합하고 씬에 반영하는 일부 작업은 메인 스레드에서 처리됩니다. 이 통합 시간이 한 프레임 안에서 길어지면, 비동기 로딩 중에도 순간적인 프레임 드롭이 보일 수 있습니다.

Unity는 이런 통합 작업이 한 프레임을 지나치게 오래 붙잡지 않도록 시간 예산을 둡니다. 이 예산은 `Application.backgroundLoadingPriority`로 조절합니다. 기본값인 `ThreadPriority.Normal`은 프레임당 비교적 큰 시간을 로딩 통합에 허용하므로 로딩은 빨리 끝나지만, 60 FPS 기준 한 프레임 예산인 약 16.7ms 중 상당 부분을 차지할 수 있습니다. 값을 `ThreadPriority.Low`로 낮추면 프레임마다 로딩에 쓰는 시간이 줄어 화면 끊김은 완화될 수 있지만, 그만큼 전체 로딩 시간은 길어집니다.

또 다른 스파이크 지점은 씬 활성화 프레임입니다. `allowSceneActivation`을 `true`로 바꾼 뒤 새 씬이 실제로 활성화되면, 그 씬의 오브젝트들이 생명주기 콜백을 실행합니다. 이때 `Awake`, `OnEnable`, `Start`에서 대량 생성, 동기 로드, 복잡한 초기화를 한꺼번에 수행하면 로딩 작업과 별개로 프레임 드롭이 생깁니다.

이 비용은 `backgroundLoadingPriority`로 줄일 수 없습니다. 활성화 이후에 실행되는 사용자 코드의 비용이기 때문입니다. 무거운 초기화는 코루틴이나 async 흐름으로 여러 프레임에 나누고, 가능하면 로딩 화면 중에 미리 준비하거나 실제로 필요해지는 시점까지 늦추는 식으로 따로 관리해야 합니다.

---

## Additive 씬 로딩

지금까지의 씬 로딩은 새 씬이 기존 씬을 대체하는 흐름이었습니다. `LoadSceneMode.Single`로 씬을 로드하면 이전 씬은 언로드되고, 그 씬에 있던 GameObject들은 파괴됩니다. 전환이 끝난 뒤 실행 중인 씬은 새로 로드한 씬 하나만 남습니다.

`LoadSceneMode.Additive`는 이 동작을 바꿉니다. 기존 씬을 내리지 않고 새 씬을 실행 중인 씬 목록에 추가합니다. 결과적으로 여러 씬이 동시에 로드되고, 각 씬에 들어 있는 오브젝트들이 같은 월드 안에서 함께 업데이트되고 렌더링됩니다.

이 방식은 화면 전체를 새 씬으로 갈아끼우는 전환이 아니라, 현재 구성 위에 씬 조각을 더하는 방식에 가깝습니다. 공통 시스템을 담은 씬은 유지하고, UI, 던전 층, 실내 공간, 보스룸 같은 콘텐츠 씬만 필요할 때 추가하거나 제거할 수 있습니다. 대신 Single 모드처럼 이전 씬이 자동으로 정리되지 않으므로, 더 이상 필요 없는 Additive 씬은 `SceneManager.UnloadSceneAsync`로 직접 내려야 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- Title -->
  <text x="350" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Single은 대체, Additive는 추가</text>

  <!-- === Left column: Single === -->
  <rect x="10" y="38" width="330" height="290" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="175" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Single: 기존 씬 대체</text>

  <!-- State 1 -->
  <text x="30" y="92" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 1</text>
  <rect x="85" y="78" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="97" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>

  <!-- Arrow + label -->
  <line x1="130" y1="106" x2="130" y2="148" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="126,145 134,145 130,153" fill="currentColor"/>
  <text x="210" y="132" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">LoadScene("B", Single)</text>

  <!-- State 2 -->
  <text x="30" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 2</text>
  <rect x="85" y="164" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>

  <!-- Destroyed Scene A -->
  <rect x="200" y="164" width="90" height="28" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <text x="245" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.3">씬 A</text>
  <line x1="208" y1="168" x2="282" y2="188" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <line x1="282" y1="168" x2="208" y2="188" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <text x="245" y="210" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">언로드됨</text>

  <!-- === Right column: Additive === -->
  <rect x="360" y="38" width="330" height="290" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Additive: 기존 씬 유지</text>

  <!-- State 1 -->
  <text x="380" y="92" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 1</text>
  <rect x="435" y="78" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="475" y="97" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>

  <!-- Arrow + label -->
  <line x1="475" y1="106" x2="505" y2="148" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="501,145 509,145 505,153" fill="currentColor"/>
  <text x="555" y="128" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Additive</text>

  <!-- State 2 -->
  <text x="380" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 2</text>
  <rect x="435" y="164" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="475" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>
  <text x="523" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="535" y="164" width="80" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="575" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>

  <!-- Arrow + label -->
  <line x1="525" y1="192" x2="545" y2="234" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="541,231 549,231 545,239" fill="currentColor"/>
  <text x="585" y="218" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Additive</text>

  <!-- State 3 -->
  <text x="380" y="264" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 3</text>
  <rect x="435" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="469" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 A</text>
  <text x="510" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="520" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="554" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 B</text>
  <text x="595" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">+</text>
  <rect x="605" y="250" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="639" y="269" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">씬 C</text>

  <text x="525" y="300" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">세 씬이 동시에 로드됨</text>
</svg>
</div>

### Additive 씬의 활용

Additive 모드는 화면을 이루는 요소를 역할별 씬으로 나눌 때 유용합니다. UI, 게임 플레이, 환경을 각각 다른 씬으로 분리하면 전체 씬을 한꺼번에 교체하지 않고 필요한 부분만 로드하거나 언로드할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- Title -->
  <text x="350" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Additive 씬 활용 예시</text>

  <!-- === Example 1: UI와 게임 분리 === -->
  <rect x="10" y="38" width="330" height="350" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>
  <text x="175" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예시 1: UI와 게임 분리</text>

  <!-- Base Scene -->
  <rect x="25" y="70" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="90" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Base Scene (항상 로드)</text>
  <text x="40" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">게임 매니저</text>
  <text x="155" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이벤트 시스템</text>
  <text x="305" y="90" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">고정</text>

  <!-- UI Scene -->
  <rect x="25" y="150" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="170" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">UI Scene (Additive)</text>
  <text x="40" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Canvas</text>
  <text x="110" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">HUD, 메뉴, 인벤토리</text>
  <text x="305" y="170" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">Additive</text>

  <!-- GamePlay Scene -->
  <rect x="25" y="230" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="250" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GamePlay Scene (Additive)</text>
  <text x="40" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">카메라</text>
  <text x="95" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">조명</text>
  <text x="135" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">플레이어, 적, 환경</text>
  <text x="305" y="250" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">Additive</text>

  <!-- Bracket showing all loaded -->
  <text x="175" y="325" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">세 씬이 동시에 활성화</text>

  <!-- === Example 2: 던전/스테이지 분리 === -->
  <rect x="360" y="38" width="330" height="350" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예시 2: 던전/스테이지 분리</text>

  <!-- Persistent Scene -->
  <rect x="375" y="70" width="300" height="70" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="90" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Persistent Scene</text>
  <text x="390" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">플레이어</text>
  <text x="465" y="108" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">UI</text>
  <text x="655" y="90" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">항상 유지</text>

  <!-- Arrow down -->
  <line x1="525" y1="140" x2="525" y2="158" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="521,155 529,155 525,163" fill="currentColor"/>

  <!-- Dungeon Floor 1 (active, solid) -->
  <rect x="375" y="165" width="300" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="185" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Dungeon_Floor_1</text>
  <text x="655" y="185" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">현재 로드</text>
  <text x="390" y="203" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">현재 층의 지형, 적, 오브젝트</text>

  <!-- Swap arrows -->
  <line x1="525" y1="227" x2="525" y2="260" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <polygon points="521,255 529,255 525,263" fill="currentColor" opacity="0.6"/>
  <polygon points="521,232 529,232 525,225" fill="currentColor" opacity="0.6"/>
  <text x="548" y="248" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">교체</text>

  <!-- Dungeon Floor 2 (dashed, next) -->
  <rect x="375" y="265" width="300" height="62" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="390" y="285" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.6">Dungeon_Floor_2</text>
  <text x="655" y="285" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">다음 층 진입 시</text>
  <text x="390" y="303" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">다음 층의 지형, 적, 오브젝트</text>

  <text x="525" y="355" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Persistent Scene은 유지, 콘텐츠 씬만 교체</text>
</svg>
</div>

### SetActiveScene

Additive로 여러 씬을 동시에 로드하면, 새로 생성되는 오브젝트를 어느 씬에 넣을지 정해야 합니다. 씬이 하나뿐일 때는 드러나지 않던 문제지만, UI 씬과 게임 플레이 씬이 함께 올라와 있는 상태라면 `Instantiate`나 `new GameObject`로 만든 오브젝트의 소속 씬이 의미를 갖습니다.

이 기본 소속을 정하는 기준이 **Active Scene**입니다. 이름 때문에 현재 실행 중인 씬 하나만 가리키는 것처럼 보일 수 있지만, Additive로 로드된 씬들은 모두 함께 실행됩니다. 여기서 Active Scene은 새 GameObject가 들어갈 기본 대상 씬이고, 동시에 전역 환경 설정을 가져오는 기준 씬입니다. 어느 씬을 Active Scene으로 둘지는 `SceneManager.SetActiveScene(scene)`으로 바꿉니다.

<br>

```csharp
// 로드된 씬: UI Scene, GamePlay Scene
// Active Scene: GamePlay Scene

var bullet = Instantiate(bulletPrefab);
// bullet은 GamePlay Scene에 생성됨

SceneManager.SetActiveScene(uiScene);

var tooltip = Instantiate(tooltipPrefab);
// tooltip은 UI Scene에 생성됨
```

<br>

코드에서 보듯 같은 `Instantiate` 호출이라도 Active Scene이 어디냐에 따라 생성 결과가 다른 씬에 들어갑니다. 다만 `SetActiveScene`은 이후 생성될 오브젝트의 기본 소속을 바꾸는 호출입니다. 이미 만들어진 오브젝트의 소속 씬을 옮기지는 않습니다. 기존 오브젝트를 다른 씬으로 옮겨야 한다면 `SceneManager.MoveGameObjectToScene`을 따로 사용합니다.

Active Scene을 맞춰 두어야 하는 첫 번째 이유는 언로드 범위입니다. 특정 씬을 언로드하면 그 씬에 속한 오브젝트가 함께 정리됩니다. 총알, 이펙트, 임시 UI처럼 콘텐츠 씬과 함께 사라져야 하는 오브젝트가 다른 씬에 생성되면 언로드 뒤에도 남을 수 있고, 반대로 계속 유지되어야 할 오브젝트가 콘텐츠 씬에 들어가면 씬을 내릴 때 함께 사라질 수 있습니다.

두 번째 이유는 전역 환경 설정입니다. 라이트맵처럼 씬별로 저장되는 데이터는 각 씬에 묶여 있지만, 환경 조명, 스카이박스, 포그처럼 화면 전체에 적용되는 설정은 Active Scene의 값을 기준으로 삼습니다. 콘텐츠 씬을 교체했는데 Active Scene을 새 씬으로 옮기지 않으면, 오브젝트는 새 씬의 것이지만 환경 설정은 이전 씬의 값으로 남아 어색한 화면이 나올 수 있습니다.

---

## DontDestroyOnLoad

`LoadSceneMode.Single`로 씬을 전환하면 이전 씬에 있던 오브젝트는 파괴됩니다. 하지만 게임 실행 동안 계속 유지되어야 하는 오브젝트도 있습니다. 점수와 진행도를 관리하는 GameManager, BGM을 이어서 재생하는 AudioManager, 서버 연결을 유지하는 NetworkManager처럼 씬이 바뀌어도 사라지면 안 되는 시스템 오브젝트입니다.

이런 오브젝트를 씬 전환의 파괴 대상에서 제외하는 호출이 `DontDestroyOnLoad(gameObject)`입니다. 한 번 호출하면 해당 오브젝트는 다음 씬으로 전환될 때도 파괴되지 않고 유지됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 530" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">DontDestroyOnLoad의 동작</text>

  <!-- === 씬 전환 전 === -->
  <text x="20" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 전환 전</text>
  <rect x="10" y="56" width="580" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Menu Scene</text>

  <!-- MenuUI -->
  <rect x="80" y="90" width="170" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">MenuUI</text>
  <text x="165" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">일반 오브젝트</text>

  <!-- GameManager (highlighted) -->
  <rect x="330" y="90" width="200" height="56" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="430" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>
  <text x="430" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">DDOL* 적용</text>

  <!-- Transition arrow -->
  <line x1="300" y1="166" x2="300" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="296,207 304,207 300,215" fill="currentColor"/>
  <text x="320" y="192" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">씬 전환 (LoadScene Single)</text>

  <!-- === 씬 전환 후 === -->
  <text x="20" y="234" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 전환 후</text>

  <!-- Destroyed MenuUI (독립 요소) -->
  <rect x="30" y="248" width="140" height="28" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.25"/>
  <text x="100" y="266" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.25">MenuUI</text>
  <line x1="38" y1="252" x2="162" y2="272" stroke="currentColor" stroke-width="1.2" opacity="0.3"/>
  <line x1="162" y1="252" x2="38" y2="272" stroke="currentColor" stroke-width="1.2" opacity="0.3"/>
  <text x="185" y="266" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">파괴됨</text>

  <!-- DDOL Scene -->
  <rect x="10" y="290" width="580" height="68" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="24" y="310" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontDestroyOnLoad (별도 씬)</text>

  <rect x="30" y="318" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="338" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>

  <text x="255" y="338" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">파괴되지 않고 유지</text>

  <!-- Arrow from old GameManager to DDOL -->
  <line x1="430" y1="146" x2="430" y2="200" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <line x1="430" y1="200" x2="130" y2="318" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <polygon points="126,316 134,316 130,323" fill="currentColor" opacity="0.5"/>

  <!-- GamePlay Scene -->
  <rect x="10" y="372" width="580" height="86" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="392" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GamePlay Scene</text>

  <rect x="80" y="402" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="427" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Player</text>

  <rect x="330" y="402" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="427" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Environment</text>

  <!-- Summary notes -->
  <text x="300" y="482" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">MenuUI는 씬 전환 시 파괴됨</text>
  <text x="300" y="498" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GameManager는 DontDestroyOnLoad 씬으로 이동하여 유지</text>
  <text x="300" y="516" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">* DDOL = DontDestroyOnLoad</text>
</svg>
</div>

`DontDestroyOnLoad`가 호출된 오브젝트는 원래 씬에 남아 있는 것이 아니라, Unity가 내부적으로 관리하는 **DontDestroyOnLoad 씬**으로 옮겨집니다. 그래서 이후 `LoadSceneMode.Single`로 다른 씬을 로드해도 기존 씬의 언로드 대상에 포함되지 않습니다. 런타임에 `gameObject.scene.name`을 확인하면 `"DontDestroyOnLoad"`라는 이름을 볼 수 있고, Hierarchy 창에서도 이 별도 씬을 확인할 수 있습니다.

적용 대상은 **루트 GameObject**입니다. 루트에 `DontDestroyOnLoad`를 한 번 적용하면 그 아래 자식들도 함께 유지됩니다. 반대로 자식 오브젝트를 직접 넘기면 호출은 적용되지 않고, Unity는 루트 GameObject나 루트의 컴포넌트에만 동작한다는 경고를 출력합니다. 따라서 유지해야 하는 묶음이 있다면, 그 묶음의 루트에만 호출을 둡니다.

필요하다면 DontDestroyOnLoad 씬에 들어간 오브젝트를 다시 일반 씬으로 옮길 수도 있습니다. 이때는 `SceneManager.MoveGameObjectToScene(gameObject, targetScene)`을 사용합니다. 이 메서드 역시 루트 GameObject를 대상으로 하므로 자식을 넘기면 예외가 발생합니다. 전역으로 유지하던 오브젝트를 특정 씬의 수명에 다시 묶고 싶다면, 대상 씬으로 옮긴 뒤 그 씬이 언로드될 때 함께 정리되도록 만들 수 있습니다.

### 일반적인 사용 대상

DontDestroyOnLoad는 게임 실행 동안 계속 유지되어야 하는 시스템 성격의 오브젝트에 적합합니다. 반대로 특정 씬에서만 잠시 사용하는 오브젝트에는 적용하지 않는 편이 좋습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">DontDestroyOnLoad 대표 사용처</text>

  <!-- === 적합한 사용처 (upper, green-ish via low opacity) === -->
  <rect x="10" y="38" width="540" height="206" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">적합한 사용처</text>

  <!-- Item 1 -->
  <rect x="25" y="74" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="94" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GameManager</text>
  <text x="200" y="94" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">게임 상태 관리 (점수, 진행도)</text>

  <!-- Item 2 -->
  <rect x="25" y="110" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="130" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">AudioManager</text>
  <text x="200" y="130" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">BGM 끊김 없이 재생</text>

  <!-- Item 3 -->
  <rect x="25" y="146" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="166" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">NetworkManager</text>
  <text x="200" y="166" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">서버 연결 유지</text>

  <!-- Item 4 -->
  <rect x="25" y="182" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="202" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">InputManager</text>
  <text x="200" y="202" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">입력 설정 유지</text>

  <!-- Item 5 -->
  <rect x="25" y="218" width="510" height="30" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="238" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">EventSystem</text>
  <text x="200" y="238" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">UI 이벤트 처리 (주의: 중복 방지 필요)</text>

  <!-- === 부적합한 사용처 (lower, red-ish via higher opacity) === -->
  <rect x="10" y="258" width="540" height="120" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="282" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">부적합한 사용처</text>

  <!-- Item 1 -->
  <rect x="25" y="292" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="310" font-family="sans-serif" font-size="11" fill="currentColor">특정 씬에서만 필요한 오브젝트</text>

  <!-- Item 2 -->
  <rect x="25" y="322" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="340" font-family="sans-serif" font-size="11" fill="currentColor">임시 데이터를 가진 오브젝트</text>

  <!-- Item 3 -->
  <rect x="25" y="352" width="510" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="370" font-family="sans-serif" font-size="11" fill="currentColor">UI 요소 (특정 화면의 UI)</text>
</svg>
</div>

그림에서 EventSystem에 "중복 방지 필요"라고 적은 이유는 수명보다 개수가 더 중요한 오브젝트이기 때문입니다. EventSystem을 DontDestroyOnLoad로 유지했는데 새 씬에도 EventSystem이 배치되어 있으면, 씬 전환 뒤에는 EventSystem이 둘 이상 남습니다. UI 입력은 하나의 EventSystem을 기준으로 처리되어야 하므로, 이런 오브젝트는 전역으로 유지할지 씬마다 둘지를 먼저 정하고 중복 인스턴스가 생기지 않게 관리해야 합니다.

부적합한 대상도 같은 기준으로 판단합니다. 특정 화면에서만 필요한 UI 패널, 특정 전투에서만 쓰는 임시 데이터, 한 번 재생되고 사라질 이펙트처럼 수명이 짧거나 특정 씬에 묶인 오브젝트는 DontDestroyOnLoad에 올리지 않는 편이 맞습니다. 이런 오브젝트가 씬 전환 뒤에도 살아남으면 더 이상 쓰이지 않는 상주 객체가 되고, 참조하고 있던 에셋까지 함께 메모리에 남길 수 있습니다.

### 싱글턴 중복 인스턴스 문제

EventSystem에서 본 중복 문제는 싱글턴 매니저에서도 자주 생깁니다. DontDestroyOnLoad로 유지하는 매니저는 보통 게임 전체에 하나만 있어야 하지만, 그 매니저가 씬 안에 배치되어 있다면 씬을 다시 로드할 때 새 인스턴스가 다시 만들어집니다.

예를 들어 씬 A에 GameManager가 있고, 첫 실행 때 이 오브젝트를 DontDestroyOnLoad로 올렸다고 가정해 보겠습니다. 이후 다른 씬을 거쳐 다시 씬 A를 로드하면, 씬 A에 배치된 GameManager가 새로 생성됩니다. 기존 GameManager는 DontDestroyOnLoad 씬에 남아 있으므로, 결과적으로 같은 역할의 매니저가 두 개가 됩니다.

이 문제는 씬 전환 코드가 아니라 매니저 자신이 방어하는 편이 안전합니다. `Awake`에서 이미 등록된 인스턴스가 있는지 먼저 확인하고, 기존 인스턴스가 있다면 새로 만들어진 자신을 즉시 파괴합니다. 기존 인스턴스가 없을 때만 자신을 전역 인스턴스로 등록하고 DontDestroyOnLoad에 올리는 식입니다. 이렇게 해야 어떤 씬에서 시작하든 매니저가 하나만 유지됩니다.

### 남용 시 메모리 상주 위험

중복만큼 자주 문제가 되는 것이 메모리입니다. DontDestroyOnLoad 자체가 곧바로 메모리 누수를 만드는 것은 아닙니다. 문제는 이 오브젝트가 오래 살아남는 만큼, 이 오브젝트가 잡고 있는 참조도 오래 살아남는다는 점입니다.

전역 매니저가 큰 텍스처, 오디오 클립, 프리팹을 필드로 직접 참조하고 있으면 Unity 입장에서는 그 에셋이 여전히 사용 중인 상태입니다. 씬을 언로드하거나 `Resources.UnloadUnusedAssets()`가 실행되어도, 살아 있는 DontDestroyOnLoad 오브젝트에서 참조가 이어져 있다면 해당 에셋은 해제 대상이 되지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- AudioManager 루트 박스 -->
  <rect x="145" y="10" width="230" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="30" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">AudioManager</text>
  <text x="260" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(DontDestroyOnLoad)</text>

  <!-- 중앙 수직선 -->
  <line x1="260" y1="54" x2="260" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <!-- 수평 분기선 -->
  <line x1="70" y1="78" x2="450" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <!-- 각 노드로 수직선 + 화살표 -->
  <line x1="70" y1="78" x2="70" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="67,96 70,102 73,96" fill="currentColor"/>
  <line x1="197" y1="78" x2="197" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="194,96 197,102 200,96" fill="currentColor"/>
  <line x1="323" y1="78" x2="323" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="320,96 323,102 326,96" fill="currentColor"/>
  <line x1="450" y1="78" x2="450" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="447,96 450,102 453,96" fill="currentColor"/>

  <!-- BGM 1: MainMenu -->
  <rect x="10" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_MainMenu</text>
  <text x="70" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (3MB)</text>
  <text x="70" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메인 메뉴에서만 필요</text>

  <!-- BGM 2: GamePlay -->
  <rect x="137" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="197" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_GamePlay</text>
  <text x="197" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (5MB)</text>
  <text x="197" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">게임 중에만 필요</text>

  <!-- BGM 3: Boss -->
  <rect x="263" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="323" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_Boss</text>
  <text x="323" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (4MB)</text>
  <text x="323" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">보스전에서만 필요</text>

  <!-- BGM 4: Ending -->
  <rect x="390" y="104" width="120" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">BGM_Ending</text>
  <text x="450" y="139" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">.ogg (3MB)</text>
  <text x="450" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">엔딩에서만 필요</text>

  <!-- 구분선 -->
  <line x1="30" y1="190" x2="490" y2="190" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 합계 강조 박스 -->
  <rect x="130" y="204" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="220" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">3 + 5 + 4 + 3 = 15MB</text>
  <text x="260" y="234" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">항상 메모리에 상주</text>

  <!-- 화살표: 합계 → 해결 -->
  <line x1="260" y1="240" x2="260" y2="260" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="257,260 260,266 263,260" fill="currentColor"/>

  <!-- 해결 방안 박스 (점선) -->
  <rect x="80" y="268" width="360" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="260" y="288" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">해결: BGM을 직접 참조하지 않고</text>
  <text x="260" y="306" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">필요 시 Addressables로 동적 로드/해제</text>

  <!-- 보조 텍스트 -->
  <text x="260" y="350" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">DDOL 오브젝트가 에셋을 직접 참조하면 씬 전환과 무관하게 메모리 점유</text>
</svg>
</div>

그림의 예처럼 AudioManager가 메뉴, 게임, 보스, 엔딩 BGM을 모두 직접 참조하면 현재 한 곡만 재생하더라도 네 개의 오디오 클립이 모두 AudioManager를 통해 도달 가능한 상태로 남습니다. 씬이 바뀌어도 AudioManager는 유지되므로, 그 참조를 끊지 않는 한 클립들도 계속 메모리에 머무를 수 있습니다.

따라서 DontDestroyOnLoad 오브젝트는 가능한 한 가볍게 유지하는 편이 좋습니다. 전역 매니저는 재생 상태, 설정, 로딩 흐름처럼 오래 유지되어야 하는 데이터와 기능만 갖고, 실제 콘텐츠 에셋은 필요해지는 시점에 따로 로드하는 구조가 낫습니다.

Addressables 같은 동적 로딩을 사용하면 메뉴 BGM은 메뉴에서만 로드하고, 보스 BGM은 보스전에 들어갈 때 로드한 뒤 사용이 끝났을 때 해제할 수 있습니다. 인스펙터 필드로 직접 참조해야 한다면, 게임 전체에서 계속 필요한 에셋인지 먼저 확인해야 합니다. DontDestroyOnLoad 오브젝트를 전역 콘텐츠 보관함처럼 쓰기 시작하면 씬 전환으로 정리될 수 있는 리소스까지 함께 붙잡게 됩니다.

---

## 씬 언로딩과 메모리 해제

씬을 언로드하면 먼저 그 씬에 속한 GameObject와 컴포넌트가 정리됩니다. 하지만 이것만으로 그 오브젝트들이 참조하던 텍스처, 메쉬, 오디오 클립까지 곧바로 메모리에서 내려가는 것은 아닙니다.

Unity에서 씬 언로딩은 **오브젝트 파괴**와 **에셋 해제**가 나뉘어 진행됩니다. 화면에서 오브젝트가 사라졌다는 것은 더 이상 그 오브젝트가 실행되지 않는다는 뜻이지, 관련 에셋의 참조가 모두 끊어졌다는 뜻은 아닙니다. 같은 에셋을 다른 씬이나 DontDestroyOnLoad 오브젝트가 여전히 참조하고 있다면, 그 에셋은 계속 메모리에 남아야 합니다.

### 오브젝트 파괴 vs 에셋 해제

씬 언로드의 첫 번째 결과는 오브젝트 파괴입니다. 언로드되는 씬에 속한 GameObject와 컴포넌트가 제거되고, 활성 상태였던 오브젝트에는 `OnDisable`과 `OnDestroy`가 호출됩니다. 그 오브젝트에서 실행 중이던 **코루틴(Coroutine)**도 함께 멈춥니다. 코루틴은 MonoBehaviour에 묶여 실행되므로, 대상 MonoBehaviour가 사라지면 더 이상 이어서 실행될 주체가 없습니다.

하지만 오브젝트가 외부 시스템에 남긴 연결까지 모두 사라지는 것은 아닙니다. 이벤트 발행자가 DontDestroyOnLoad 오브젝트나 정적 이벤트처럼 계속 살아 있다면, 파괴된 오브젝트의 메서드가 델리게이트에 남을 수 있습니다. 이 상태에서 콜백이 호출되면 이미 파괴된 Unity 오브젝트에 접근하게 되므로, 직접 등록한 이벤트 구독은 `OnDisable`이나 `OnDestroy`에서 해제해 두는 편이 안전합니다.

여기까지는 오브젝트의 생명주기 정리입니다. 텍스처, 메쉬, 오디오 클립 같은 에셋 메모리는 별도 기준으로 처리됩니다. 방금 파괴된 오브젝트가 참조를 놓았더라도, 같은 에셋을 다른 씬이나 전역 오브젝트가 여전히 참조하고 있다면 그 에셋은 계속 필요하기 때문입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 타이틀 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 언로드와 에셋 해제</text>

  <!-- ===== 단계 1: 오브젝트 파괴 ===== -->
  <rect x="10" y="34" width="540" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="56" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">단계 1, 오브젝트 파괴</text>

  <!-- GO 박스들 (파괴됨) -->
  <rect x="30" y="68" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="90" y="89" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Player (파괴)</text>

  <rect x="30" y="108" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="90" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy (파괴)</text>

  <rect x="30" y="148" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="100" y="169" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Environment (파괴)</text>

  <!-- 괄호 + 콜백 텍스트 -->
  <line x1="180" y1="78" x2="195" y2="78" stroke="currentColor" stroke-width="1"/>
  <line x1="180" y1="124" x2="195" y2="124" stroke="currentColor" stroke-width="1"/>
  <line x1="180" y1="164" x2="195" y2="164" stroke="currentColor" stroke-width="1"/>
  <line x1="195" y1="78" x2="195" y2="164" stroke="currentColor" stroke-width="1"/>
  <line x1="195" y1="124" x2="210" y2="124" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,121 216,124 210,127" fill="currentColor"/>
  <text x="222" y="128" font-family="sans-serif" font-size="10" fill="currentColor">OnDisable, OnDestroy 호출</text>

  <!-- 에셋 잔류 표시 -->
  <rect x="370" y="68" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="89" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Texture_A</text>

  <rect x="370" y="108" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Mesh_B</text>

  <rect x="370" y="148" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="169" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Audio_C</text>

  <text x="450" y="198" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">아직 메모리에 남음</text>

  <!-- 단계 1→2 화살표 -->
  <line x1="280" y1="214" x2="280" y2="244" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="277,244 280,250 283,244" fill="currentColor"/>

  <!-- ===== 단계 2: 에셋 해제 ===== -->
  <rect x="10" y="254" width="540" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="276" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">단계 2, 참조 검사 후 에셋 해제</text>

  <!-- UnloadUnusedAssets 호출 박스 -->
  <rect x="30" y="290" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="185" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Resources.UnloadUnusedAssets()</text>

  <!-- 화살표 → 해제 결과 -->
  <line x1="345" y1="305" x2="370" y2="305" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,302 376,305 370,308" fill="currentColor"/>

  <!-- 해제 결과 텍스트 -->
  <text x="382" y="298" font-family="sans-serif" font-size="10" fill="currentColor">참조 없는 에셋 해제:</text>
  <text x="382" y="314" font-family="sans-serif" font-size="10" fill="currentColor">Texture_A, Mesh_B, Audio_C</text>

  <!-- 해제 완료 아이콘 표시 (점선 박스) -->
  <rect x="370" y="330" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="450" y="344" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Texture_A, 해제됨</text>
  <text x="450" y="356" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Mesh_B, Audio_C, 해제됨</text>

  <!-- 주의 텍스트 -->
  <rect x="30" y="334" width="320" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="40" y="352" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">※ 다른 씬이나 DDOL 오브젝트가 참조 중이면 해제되지 않음</text>

  <!-- 하단 보조 텍스트 -->
  <text x="280" y="440" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">오브젝트 파괴와 에셋 메모리 해제는 별도 과정</text>
</svg>
</div>

그림에서 보듯 1단계에서 Player, Enemy, Environment가 파괴되어도 Texture_A, Mesh_B, Audio_C가 곧바로 내려가는 것은 아닙니다. 파괴된 오브젝트의 참조는 사라졌지만, 같은 에셋을 다른 씬이나 DontDestroyOnLoad 오브젝트가 잡고 있을 수 있기 때문입니다.

그래서 에셋 해제에는 참조 검사 단계가 필요합니다. `Resources.UnloadUnusedAssets()`는 메모리에 올라온 에셋 중 더 이상 도달 가능한 참조가 없는 것만 찾아서 내립니다. 반대로 살아 있는 오브젝트가 하나라도 참조하고 있는 에셋은 씬 언로드 뒤에도 유지됩니다.

### Resources.UnloadUnusedAssets()

`Resources.UnloadUnusedAssets()`는 현재 메모리에 올라와 있지만 더 이상 사용되지 않는 에셋을 찾아 내리는 함수입니다. Unity는 씬 계층, DontDestroyOnLoad 씬, 컴포넌트 필드, 정적 필드처럼 살아 있는 객체에서 도달할 수 있는 참조를 따라가며 에셋이 아직 필요한지 판단합니다.

이 검사에서 어떤 살아 있는 객체도 더 이상 참조하지 않는 에셋만 해제 대상이 됩니다. 반대로 한 곳에서라도 참조가 남아 있다면, 그 에셋은 씬 언로드 이후에도 유지됩니다. 그래서 이 함수는 "메모리를 전부 비우는 호출"이 아니라 "참조가 끊긴 에셋만 정리하는 호출"로 이해하는 편이 맞습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">UnloadUnusedAssets()의 기준</text>

  <!-- Outer border -->
  <rect x="10" y="38" width="540" height="156" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>

  <!-- Header background -->
  <rect x="11" y="39" width="538" height="26" fill="currentColor" fill-opacity="0.08"/>

  <!-- Header texts -->
  <text x="85" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋</text>
  <text x="290" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">참조 상태</text>
  <text x="490" y="57" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">결과</text>

  <!-- Header bottom line -->
  <line x1="10" y1="65" x2="550" y2="65" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Column separators -->
  <line x1="165" y1="39" x2="165" y2="193" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <line x1="430" y1="39" x2="430" y2="193" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- Row 1: Texture_A, 해제 -->
  <text x="85" y="86" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor" opacity="0.4">Texture_A</text>
  <text x="290" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">참조 없음</text>
  <text x="490" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">해제</text>

  <line x1="10" y1="97" x2="550" y2="97" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 2: Texture_B, 유지 -->
  <rect x="11" y="98" width="538" height="31" fill="currentColor" fill-opacity="0.04"/>
  <text x="85" y="118" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">Texture_B</text>
  <text x="290" y="118" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Player가 참조</text>
  <text x="490" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">유지</text>

  <line x1="10" y1="129" x2="550" y2="129" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 3: Mesh_C, 해제 -->
  <text x="85" y="150" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor" opacity="0.4">Mesh_C</text>
  <text x="290" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">참조 없음</text>
  <text x="490" y="150" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">해제</text>

  <line x1="10" y1="161" x2="550" y2="161" stroke="currentColor" stroke-width="0.5" opacity="0.1"/>

  <!-- Row 4: Audio_D, 유지 -->
  <rect x="11" y="162" width="538" height="31" fill="currentColor" fill-opacity="0.04"/>
  <text x="85" y="182" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">Audio_D</text>
  <text x="290" y="182" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">AudioManager가 참조 (DDOL)</text>
  <text x="490" y="182" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">유지</text>

  <!-- Footer -->
  <text x="280" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">AsyncOperation 반환 · 참조 검사 비용 존재</text>
  <text x="280" y="238" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로딩 화면이나 전환 구간에서 호출하는 편이 안전</text>
</svg>
</div>

호출 결과는 `AsyncOperation`으로 돌아오므로 비동기 흐름에 넣을 수 있습니다. 다만 비동기라고 해서 비용이 없는 것은 아닙니다. 참조 관계를 검사하고 해제 대상을 정리하는 작업 자체는 프로젝트에 로드된 에셋과 객체가 많을수록 무거워질 수 있습니다.

따라서 이 함수는 게임 플레이 중에 자주 호출할 함수가 아닙니다. 씬 전환 중 로딩 화면을 띄운 상태, 큰 콘텐츠 묶음을 언로드한 직후, 또는 메모리를 정리해도 화면 멈춤을 감출 수 있는 구간에서 호출하는 편이 좋습니다. 확인해야 할 대상이 많은 프로젝트일수록 한 번 실행하는 비용이 커지므로, 매 프레임 호출하는 식의 사용은 피해야 합니다.

### GC.Collect와의 관계

`Resources.UnloadUnusedAssets()`와 `GC.Collect()`는 둘 다 메모리 정리와 관련이 있지만, 정리하는 대상이 다릅니다. **가비지 컬렉션(Garbage Collection)**은 C#의 **관리 힙(Managed Heap)**을 검사해, 코드 어디에서도 더 이상 도달할 수 없는 객체를 수거합니다. `GC.Collect()`는 이 수거 작업을 즉시 요청하는 함수입니다.

반면 `UnloadUnusedAssets()`는 Unity 에셋 쪽을 정리합니다. 텍스처의 픽셀 데이터, 메쉬의 정점 데이터, 오디오 데이터처럼 실제 에셋 데이터는 네이티브 메모리에 있고, C#에서는 `Texture2D`, `Mesh`, `AudioClip` 같은 관리 래퍼를 통해 그 데이터를 가리킵니다. `GC.Collect()`만 호출한다고 해서 이런 네이티브 에셋 메모리가 내려가는 것은 아닙니다.

두 정리 작업이 서로 영향을 주는 지점은 이 관리 래퍼입니다. 살아 있는 C# 객체가 `Texture2D`나 `Mesh` 래퍼를 참조하고 있으면, Unity는 그 에셋을 아직 사용할 수 있는 상태로 봅니다. 따라서 에셋을 내리려면 네이티브 데이터만 보는 것이 아니라, 살아 있는 관리 객체에서 해당 에셋으로 이어지는 참조가 남아 있는지도 함께 중요해집니다.

씬을 언로드하면 GameObject와 컴포넌트의 네이티브 오브젝트는 파괴됩니다. Unity의 특수한 null 비교에서는 이 객체들이 `== null`처럼 보일 수 있습니다. 하지만 C# 래퍼 객체 자체는 관리 힙에 남아 있을 수 있고, 다른 관리 객체나 정적 필드가 그 래퍼를 계속 붙잡고 있다면 가비지 컬렉터도 수거하지 않습니다.

그 래퍼가 다시 `Texture2D`, `Mesh`, `AudioClip` 같은 에셋 래퍼를 참조하고 있다면, 에셋도 도달 가능한 상태로 남습니다. 이 경우 `UnloadUnusedAssets()`를 호출해도 해당 에셋은 사용 중인 것으로 판단되어 유지됩니다. 결국 관리 힙의 참조 정리가 제대로 되어 있지 않으면, 에셋 해제 결과에도 영향을 줄 수 있습니다.

그렇다고 씬 전환마다 `GC.Collect()`를 따로 호출하는 습관을 들일 필요는 없습니다. `GC.Collect()`도 프레임을 멈출 수 있는 무거운 작업이고, `UnloadUnusedAssets()` 역시 별도 비용이 큽니다. 보통은 참조를 명확히 끊고, 큰 씬 전환이나 로딩 화면처럼 멈춤을 감출 수 있는 구간에서 `UnloadUnusedAssets()`를 호출한 뒤, 실제로 관리 힙 문제가 남는지는 프로파일러로 확인하는 편이 좋습니다.

### 씬 전환 시 전체 흐름

앞에서 본 내용을 실제 씬 전환에 적용하면 핵심은 순서입니다. 메모리 여유가 충분한 전환이라면 새 씬을 먼저 로드한 뒤 이전 씬을 내리는 방식도 사용할 수 있습니다. 하지만 이전 씬과 새 씬의 에셋 규모가 크다면, 두 씬의 에셋이 동시에 올라오는 순간에 메모리 피크가 크게 튈 수 있습니다.

이 피크를 낮추려면 로딩 화면을 중간에 두고 전환을 단계로 나누는 편이 낫습니다. 먼저 로딩 화면만 남길 수 있는 상태를 만든 뒤, 이전 씬을 언로드하고, 더 이상 참조되지 않는 에셋을 정리한 다음 새 씬을 로드합니다. 이렇게 하면 새 씬의 에셋을 올리기 전에 이전 씬에서만 쓰던 에셋을 내릴 기회를 만들 수 있습니다.

> 메모리 피크 관리는 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 자세히 다룹니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- ===== 상단: 5단계 순서도 ===== -->
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메모리 피크를 낮추는 전환 흐름</text>

  <!-- 단계 1 -->
  <rect x="10" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="64" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 로딩 씬</text>
  <text x="64" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Additive 로드</text>
  <text x="64" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">로딩 화면 표시</text>

  <!-- 화살표 1→2 -->
  <line x1="118" y1="64" x2="138" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="138,61 144,64 138,67" fill="currentColor"/>

  <!-- 단계 2 -->
  <rect x="146" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 이전 씬</text>
  <text x="200" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">언로드</text>
  <text x="200" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">오브젝트 파괴</text>

  <!-- 화살표 2→3 -->
  <line x1="254" y1="64" x2="274" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="274,61 280,64 274,67" fill="currentColor"/>

  <!-- 단계 3 -->
  <rect x="282" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="336" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 미사용</text>
  <text x="336" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에셋 정리</text>
  <text x="336" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">UnloadUnusedAssets</text>

  <!-- 화살표 3→4 -->
  <line x1="390" y1="64" x2="410" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="410,61 416,64 410,67" fill="currentColor"/>

  <!-- 단계 4 -->
  <rect x="418" y="30" width="108" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="472" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4. 새 씬</text>
  <text x="472" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">비동기 로드</text>
  <text x="472" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">progress 로딩 바</text>

  <!-- 화살표 4→5 -->
  <line x1="526" y1="64" x2="546" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="546,61 552,64 546,67" fill="currentColor"/>

  <!-- 단계 5 -->
  <rect x="554" y="30" width="56" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="582" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5.</text>
  <text x="582" y="66" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">로딩 씬</text>
  <text x="582" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">언로드</text>

  <!-- yield return 보조 텍스트 -->
  <text x="310" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">각 단계에서 yield return으로 완료를 대기 → 다음 단계가 올바른 상태에서 시작</text>

  <!-- ===== 구분선 ===== -->
  <line x1="30" y1="132" x2="590" y2="132" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== 하단: 메모리 그래프 ===== -->
  <text x="310" y="154" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">메모리 변화</text>

  <!-- Y축 -->
  <line x1="60" y1="175" x2="60" y2="420" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="300" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" transform="rotate(-90, 30, 300)">메모리</text>

  <!-- X축 -->
  <line x1="60" y1="420" x2="590" y2="420" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="442" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">시간 / 단계</text>

  <!-- 메모리 꺾은선 그래프 -->
  <!-- 기준선 (이전 씬) -->
  <polyline points="60,340 120,340 160,220 200,200 240,220 300,340 340,380 400,380 440,300 500,280 560,280 590,280"
    fill="none" stroke="currentColor" stroke-width="2"/>

  <!-- 피크 영역 음영 -->
  <polygon points="120,340 160,220 200,200 240,220 300,340 120,340"
    fill="currentColor" fill-opacity="0.08"/>

  <!-- 새 씬 로드 영역 음영 -->
  <polygon points="400,380 440,300 500,280 560,280 590,280 590,380 400,380"
    fill="currentColor" fill-opacity="0.06"/>

  <!-- 피크 레이블 -->
  <line x1="200" y1="200" x2="200" y2="178" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="200" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">피크</text>

  <!-- 단계 1 레이블: 로딩 씬 추가 -->
  <text x="140" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">① 로딩 씬</text>
  <text x="140" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">추가 로드</text>
  <line x1="140" y1="420" x2="140" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 2 레이블: 이전 씬 언로드 -->
  <text x="230" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">② 이전 씬</text>
  <text x="230" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">언로드</text>
  <line x1="230" y1="420" x2="230" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 3 레이블: 에셋 해제 -->
  <text x="340" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">③ 이전 에셋 해제</text>
  <text x="340" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메모리 여유 확보</text>
  <line x1="340" y1="380" x2="340" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 4 레이블: 새 씬 로드 -->
  <text x="470" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">④ 새 에셋 로드</text>
  <line x1="470" y1="420" x2="470" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 단계 5 레이블: 로딩 씬 제거 -->
  <text x="565" y="460" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">⑤ 로딩 씬</text>
  <text x="565" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">언로드</text>
  <line x1="565" y1="420" x2="565" y2="448" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.4"/>

  <!-- 핵심 강조 텍스트 -->
  <text x="310" y="510" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">핵심: 이전 에셋 정리 후 새 에셋 로드 → 두 씬 에셋 동시 상주 구간 축소</text>
  <text x="310" y="526" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Additive 씬 언로드만으로 에셋 메모리가 내려가지는 않음 → 필요 시 명시 정리</text>
</svg>
</div>

그림에서 중요한 지점은 3단계입니다. `UnloadSceneAsync`로 Additive 씬을 내리면 그 씬의 오브젝트는 제거되지만, 에셋 메모리까지 함께 내려간다고 볼 수는 없습니다. 이전 씬에서만 쓰던 에셋을 실제로 정리하려면 참조가 끊긴 상태에서 `Resources.UnloadUnusedAssets()`를 호출해야 합니다.

Single 모드와 Additive 모드는 여기서 차이가 납니다. `LoadSceneMode.Single`로 씬을 로드하면 Unity가 `Resources.UnloadUnusedAssets()`를 자동으로 호출합니다. 반면 Additive 씬을 `UnloadSceneAsync`로 내리는 경우에는 에셋 메모리를 비우려면 별도의 정리 단계가 필요합니다. Additive 기반 전환에서 메모리 피크를 관리하려면 이 차이를 전제로 순서를 잡아야 합니다.

각 단계 사이에서는 `yield return`이나 `await`로 앞 작업의 완료를 기다려야 합니다. `UnloadSceneAsync`, `Resources.UnloadUnusedAssets()`, `LoadSceneAsync`는 모두 완료 시점이 뒤로 밀릴 수 있는 작업입니다. 이전 씬 언로드와 에셋 정리가 끝나기 전에 새 씬 로드를 시작하면, 두 씬의 에셋이 겹쳐 올라와 피크를 낮추려던 의도가 사라집니다.

메모리 피크가 기기의 허용 범위를 넘으면 모바일에서는 **OOM(Out Of Memory)**으로 앱이 종료될 수 있습니다. 기기 전체 RAM이 4GB나 8GB라고 해도 앱 하나가 그 전부를 쓸 수 있는 것은 아닙니다. 큰 씬을 전환할 때는 평균 메모리보다 전환 순간의 최고치를 먼저 확인해야 합니다.

---

## 대규모 월드를 위한 씬 분할 전략

앞서 살펴본 흐름은 메뉴에서 게임으로, 게임에서 결과 화면으로 넘어가는 것처럼 전환 지점이 분명한 구조에 잘 맞습니다. 플레이어가 잠시 로딩 화면을 보고, 이전 씬을 정리한 뒤, 다음 씬으로 넘어가는 방식입니다.

하지만 오픈 월드나 넓은 필드에서는 문제가 달라집니다. 플레이어는 끊김 없이 이동해야 하고, 월드 전체를 한 번에 로드하기에는 지형, 오브젝트, 텍스처, 조명 데이터가 너무 큽니다. 하나의 씬에 모두 담으면 초기 로딩 시간도 길어지고, 런타임 메모리도 기기의 한계를 넘기 쉽습니다.

이때 사용하는 방식이 **씬 분할(Scene Splitting)**입니다. 월드를 여러 조각의 씬으로 나누고, 플레이어 주변처럼 지금 필요한 조각만 Additive로 로드합니다. 멀어진 조각은 언로드해 메모리에서 내려 보내고, 새로 가까워진 조각은 다시 로드합니다. 즉 씬을 화면 전환 단위가 아니라 월드를 스트리밍하는 단위로 사용하는 방식입니다.

<br>

### 그리드 기반 월드 분할

가장 단순한 분할 방식은 월드를 격자(Grid)로 나누는 것입니다. 월드 좌표를 일정한 크기의 셀로 나누고, 각 셀을 하나의 씬으로 저장합니다. 예를 들어 `Cell_11`에는 그 구역의 지형, 배치 오브젝트, 조명, 지역 전용 이펙트가 들어갑니다.

런타임에서는 플레이어가 속한 셀을 기준으로 로드할 셀 집합을 계산합니다. 현재 셀만 로드하면 경계에 다가갔을 때 다음 구역이 보이지 않으므로, 보통 현재 셀과 주변 셀까지 함께 올립니다. 아래 예시는 플레이어가 `Cell_11`에 있을 때 주변 1칸까지 포함한 3×3 범위를 Additive로 로드하는 구조입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <text x="210" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">플레이어 기준 로드 범위</text>

  <!-- 로드 범위 점선 -->
  <rect x="30" y="40" width="360" height="240" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3"/>

  <!-- Row 0 -->
  <rect x="40" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_00</text>
  <text x="95" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="155" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_01</text>
  <text x="210" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="270" y="50" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_02</text>
  <text x="325" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- Row 1 -->
  <rect x="40" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_10</text>
  <text x="95" y="171" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <!-- Cell_11 강조 -->
  <rect x="155" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="2"/>
  <text x="193" y="155" text-anchor="middle" font-family="sans-serif" font-size="15" fill="currentColor">★</text>
  <text x="230" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_11</text>
  <text x="210" y="175" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">플레이어 위치</text>
  <rect x="270" y="125" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_12</text>
  <text x="325" y="171" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- Row 2 -->
  <rect x="40" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_20</text>
  <text x="95" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="155" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_21</text>
  <text x="210" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>
  <rect x="270" y="200" width="110" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cell_22</text>
  <text x="325" y="246" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">.unity</text>

  <!-- 하단 설명 -->
  <text x="210" y="300" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">현재 셀: Cell_11</text>
  <text x="210" y="325" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로드: 현재 셀 + 주변 1칸 (3×3 = 9개 셀)</text>
  <text x="210" y="342" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">언로드 후보: 로드 범위 밖으로 멀어진 셀</text>
  <text x="210" y="362" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점선 = 로드 범위 경계</text>
</svg>
</div>

로드 범위는 게임의 카메라 거리와 이동 속도에 맞춰 정합니다. 멀리까지 보이는 3D 월드라면 주변 1칸만으로는 부족할 수 있고, 이동 속도가 빠른 게임이라면 플레이어가 셀 경계에 닿기 전에 다음 셀이 준비되어 있어야 합니다. 반대로 시야가 좁거나 이동 속도가 느린 게임에서는 더 작은 범위로도 충분할 수 있습니다.

셀 크기도 비용을 크게 바꿉니다. 셀이 너무 크면 한 번 로드할 때 필요 없는 오브젝트와 에셋까지 함께 올라와 메모리 이점이 줄어듭니다. 셀이 너무 작으면 로드와 언로드가 너무 자주 발생하고, 씬 수가 많아져 관리 비용이 늘어납니다. 따라서 셀 크기는 월드의 밀도, 시야 거리, 이동 속도, 플랫폼 메모리를 함께 보고 정해야 합니다.

### 스트리밍: 미리 로드하고 늦게 내리기

그리드로 월드를 나누었다면, 다음 문제는 플레이어 이동에 맞춰 로드 범위를 자연스럽게 옮기는 일입니다. 셀 경계에 도착한 뒤에야 다음 셀을 로드하기 시작하면 이미 늦습니다. 로딩이 끝날 때까지 빈 지형이 보이거나, 오브젝트가 뒤늦게 나타나는 팝인이 발생할 수 있습니다.

**스트리밍(Streaming)**은 이 문제를 피하기 위해 필요한 셀을 미리 준비하는 방식입니다. 플레이어가 오른쪽 셀로 이동하고 있다면, 현재 3×3 범위는 유지한 채 오른쪽 열을 먼저 비동기로 로드합니다. 새 셀이 준비되고 플레이어가 실제로 다음 셀에 들어간 뒤에야, 반대편으로 멀어진 셀을 언로드합니다. 핵심은 새 범위는 필요해지기 전에 올리고, 기존 범위는 안전해진 뒤에 내리는 것입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text x="340" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셀 스트리밍 흐름</text>

  <!-- 타임라인 축 -->
  <line x1="30" y1="52" x2="650" y2="52" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="648,48 656,52 648,56" fill="currentColor"/>
  <text x="665" y="56" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">시간</text>

  <!-- t0 마커 -->
  <line x1="110" y1="45" x2="110" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="110" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t0</text>

  <!-- t1 마커 -->
  <line x1="340" y1="45" x2="340" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="340" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t1</text>

  <!-- t2 마커 -->
  <line x1="560" y1="45" x2="560" y2="59" stroke="currentColor" stroke-width="2"/>
  <text x="560" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">t2</text>

  <!-- t0: 3x3 그리드 (Cell_00~22 모두 로드) -->
  <!-- Row 0 -->
  <rect x="50" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">00</text>
  <rect x="91" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="132" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <!-- Row 1 -->
  <rect x="50" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">10</text>
  <rect x="91" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">★11</text>
  <rect x="132" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">12</text>
  <!-- Row 2 -->
  <rect x="50" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="69" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">20</text>
  <rect x="91" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="132" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="151" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>

  <text x="110" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">3×3 모두 로드</text>
  <text x="110" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">플레이어 Cell_11 중앙</text>

  <!-- 화살표 t0→t1 -->
  <line x1="185" y1="110" x2="255" y2="110" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <polygon points="253,107 260,110 253,113" fill="currentColor"/>

  <!-- t1: 3x3 + 새 열 로딩 시작 -->
  <!-- Row 0 -->
  <rect x="275" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">00</text>
  <rect x="316" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="357" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <!-- 새로 로드 시작: 03 -->
  <rect x="398" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">03</text>
  <!-- Row 1 -->
  <rect x="275" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">10</text>
  <rect x="316" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">★11</text>
  <rect x="357" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">12</text>
  <!-- 새로 로드 시작: 13 -->
  <rect x="398" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">13</text>
  <!-- Row 2 -->
  <rect x="275" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">20</text>
  <rect x="316" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="357" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="376" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>
  <!-- 새로 로드 시작: 23 -->
  <rect x="398" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="417" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">23</text>

  <text x="350" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Cell_12 방향 이동 예측</text>
  <text x="350" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">03/13/23 미리 로드 중</text>

  <!-- 화살표 t1→t2 -->
  <line x1="448" y1="110" x2="485" y2="110" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <polygon points="483,107 490,110 483,113" fill="currentColor"/>

  <!-- t2: 새 3x3 (01~23), 00/10/20 언로드 -->
  <!-- Row 0: 00 언로드 (흐림) -->
  <rect x="495" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">00</text>
  <rect x="536" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">01</text>
  <rect x="577" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="596" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">02</text>
  <rect x="618" y="72" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="88" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">03</text>
  <!-- Row 1: 10 언로드 -->
  <rect x="495" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">10</text>
  <rect x="536" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">11</text>
  <rect x="577" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="596" y="114" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">★12</text>
  <rect x="618" y="99" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="115" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">13</text>
  <!-- Row 2: 20 언로드 -->
  <rect x="495" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="514" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.3">20</text>
  <rect x="536" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="555" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">21</text>
  <rect x="577" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="596" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">22</text>
  <rect x="618" y="126" width="38" height="24" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="637" y="142" text-anchor="middle" font-family="sans-serif" font-size="7" font-weight="bold" fill="currentColor">23</text>

  <text x="570" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">플레이어 Cell_12 진입</text>
  <text x="570" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">새 열 준비 후 왼쪽 열 언로드</text>

  <!-- 범례 -->
  <rect x="120" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="209" font-family="sans-serif" font-size="9" fill="currentColor">새로 로드</text>
  <rect x="220" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2"/>
  <text x="240" y="209" font-family="sans-serif" font-size="9" fill="currentColor">언로드</text>
  <rect x="310" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="330" y="209" font-family="sans-serif" font-size="9" fill="currentColor">로딩 중</text>
  <rect x="400" y="200" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="420" y="209" font-family="sans-serif" font-size="9" fill="currentColor">로드 유지</text>

  <!-- 하단 결론 -->
  <text x="340" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">다음 셀을 먼저 준비해 경계 진입 시 끊김을 줄임</text>
  <text x="340" y="256" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">전환 중에는 기존 범위 + 미리 로드한 셀이 함께 유지됨</text>
</svg>
</div>

위 타임라인에서 `t0`는 플레이어가 `Cell_11`에 있고 3×3 범위가 이미 로드된 상태입니다. `t1`에서는 플레이어가 `Cell_12` 방향으로 이동하고 있으므로 오른쪽 열인 `03`, `13`, `23`을 미리 로드합니다. 이때 기존 왼쪽 열인 `00`, `10`, `20`은 아직 내리지 않습니다. 새 열이 준비되기 전에 기존 셀을 내리면, 플레이어가 방향을 조금 바꾸거나 로딩이 늦어졌을 때 빈 구간이 생길 수 있기 때문입니다.

`t2`처럼 새 열 로드가 끝나고 플레이어가 `Cell_12`에 들어가면 로드 범위를 한 칸 오른쪽으로 옮깁니다. 그때 왼쪽 열은 언로드 후보가 됩니다. 실제 구현에서는 경계에 닿자마자 바로 내리기보다, 플레이어가 충분히 멀어졌을 때 내리는 식으로 약간의 여유를 두는 편이 안정적입니다. 경계 근처에서 앞뒤로 움직일 때 로드와 언로드가 반복되는 것을 막기 위해서입니다.

미리 로드할 시점은 플레이어의 이동 속도와 셀 로딩 시간을 기준으로 정합니다. 로딩에 1초가 걸리고 플레이어가 1초 안에 셀 경계에 도달할 수 있다면, 경계 직전이 아니라 그보다 앞에서 로드를 시작해야 합니다. 로딩이 늦으면 팝인이 생기고, 너무 일찍 시작하면 전환 구간에서 동시에 유지하는 셀이 많아져 메모리 피크가 커집니다.

따라서 메모리 상한을 계산할 때는 안정 상태의 3×3 범위만 보면 부족합니다. 위 예시의 안정 상태는 9개 셀이지만, `t1`처럼 새 열을 미리 로드하는 동안에는 기존 9개 셀에 3개 셀이 더해져 일시적으로 12개 셀이 메모리에 올라올 수 있습니다. 스트리밍 구조에서는 로드 범위뿐 아니라 미리 로드하는 버퍼까지 포함해 메모리 예산을 잡아야 합니다.

### 씬 간 공유 에셋 관리

셀을 씬 단위로 나누었다고 해서 에셋 중복 문제가 자동으로 해결되는 것은 아닙니다. 이웃한 셀은 같은 나무 프리팹, 바위 메쉬, 지형 텍스처, 머티리얼을 공유하는 경우가 많습니다. 이 공유 에셋을 어디에 두고 어떤 단위로 패키징하느냐에 따라 빌드 크기와 런타임 메모리가 달라집니다.

프로젝트 안의 일반 씬들이 같은 에셋 파일을 직접 참조한다면, Unity는 같은 GUID를 가리키는 에셋을 같은 대상으로 볼 수 있습니다. 문제는 셀을 AssetBundle이나 Addressables 그룹으로 나누어 배포할 때 더 자주 드러납니다. 공유 에셋을 별도 의존성으로 분리하지 않으면, 각 셀 번들 안에 같은 데이터가 반복해서 포함될 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공유 에셋의 패키징 방식</text>

  <!-- 문제 섹션 -->
  <rect x="20" y="38" width="480" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="58" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">문제: 셀 번들마다 공유 에셋을 함께 포함한 경우</text>

  <!-- Cell_11 번들 -->
  <rect x="35" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="105" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_11 번들</text>
  <text x="105" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- Cell_12 번들 -->
  <rect x="190" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_12 번들</text>
  <text x="260" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- Cell_21 번들 -->
  <rect x="345" y="70" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="415" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Cell_21 번들</text>
  <text x="415" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Tree_A (4MB)</text>

  <!-- 중복 표시 -->
  <text x="213" y="133" font-family="sans-serif" font-size="11" fill="currentColor">동일 데이터가 3개 번들에 포함</text>
  <text x="400" y="133" font-family="sans-serif" font-size="11" fill="currentColor">= 12MB</text>
  <text x="470" y="155" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">✕</text>

  <!-- 해결 섹션 -->
  <text x="260" y="195" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">공유 에셋을 한 곳에서 소유</text>

  <!-- 해결 1 -->
  <rect x="20" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="97" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 1</text>
  <text x="97" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">빌드 포함 씬</text>
  <text x="97" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">직접 참조</text>
  <text x="97" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">같은 GUID 기준</text>

  <!-- 해결 2 -->
  <rect x="183" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 2</text>
  <text x="260" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">AssetBundle</text>
  <text x="260" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">공유 번들 분리</text>
  <text x="260" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">셀 번들은 의존성만 가짐</text>

  <!-- 해결 3 -->
  <rect x="345" y="208" width="155" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="422" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">해결 3</text>
  <text x="422" y="244" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Addressables</text>
  <text x="422" y="258" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">별도 그룹 분리</text>
  <text x="422" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">참조 카운트로 수명 관리</text>

  <!-- 공통 결과 -->
  <!-- 화살표: 해결1 → 결과 -->
  <line x1="97" y1="288" x2="97" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="260" y1="288" x2="260" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="422" y1="288" x2="422" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="97" y1="300" x2="422" y2="300" stroke="currentColor" stroke-width="1"/>
  <line x1="260" y1="300" x2="260" y2="312" stroke="currentColor" stroke-width="1"/>
  <polygon points="256,310 260,318 264,310" fill="currentColor"/>

  <rect x="155" y="320" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="341" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">공유 데이터는 한 번만 로드</text>
</svg>
</div>

그림의 핵심은 Tree_A를 어느 셀이 소유하느냐입니다. Tree_A를 각 셀 번들에 함께 넣으면 `Cell_11`, `Cell_12`, `Cell_21`이 모두 같은 데이터를 자기 번들 안에 갖게 됩니다. 겉으로는 같은 나무 프리팹을 참조하는 것처럼 보여도, 패키징 결과는 세 사본이 될 수 있습니다.

해결은 공유 에셋의 소유 위치를 셀 밖으로 빼는 것입니다. Tree_A를 별도의 공유 번들이나 Addressables 그룹에 두고, 셀 번들은 그 에셋을 직접 포함하는 대신 의존성으로 참조합니다. 그러면 여러 셀이 동시에 로드되어도 실제 Tree_A 데이터는 공유 위치에서 한 번만 로드됩니다.

수명 관리도 함께 맞춰야 합니다. 공유 번들은 하나의 셀이 언로드되었다고 바로 내리면 안 됩니다. 다른 셀이 아직 Tree_A를 사용하고 있을 수 있기 때문입니다. AssetBundle을 직접 관리한다면 의존 번들의 로드와 언로드 순서를 직접 보장해야 하고, Addressables를 사용한다면 핸들과 참조 카운트를 기준으로 `Release` 시점을 맞춰야 합니다.

정리하면, 셀 씬은 지역 전용 데이터만 갖고, 여러 셀이 함께 쓰는 에셋은 별도 공유 단위로 분리하는 편이 좋습니다. 이렇게 해야 셀 스트리밍을 하면서도 같은 프리팹이나 텍스처가 셀마다 중복 로드되는 일을 줄일 수 있습니다.

> Addressables를 활용한 구체적인 방법은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 자세히 다룹니다.

### 공통 씬과 콘텐츠 씬 분리

규모가 큰 프로젝트에서는 모든 전역 오브젝트를 DontDestroyOnLoad에 올리기보다, 처음부터 별도의 씬으로 관리하는 구조를 많이 사용합니다. 게임 실행 동안 유지될 시스템은 **공통 씬(Persistent Scene)**에 두고, 스테이지나 지역에 따라 바뀌는 요소는 **콘텐츠 씬(Content Scene)**으로 분리하는 방식입니다.

공통 씬은 게임의 기준이 되는 씬입니다. 플레이어, 카메라 시스템, UI, 입력, 게임 매니저처럼 지역이 바뀌어도 계속 유지되어야 하는 오브젝트가 여기에 들어갑니다. 콘텐츠 씬은 교체 가능한 부분입니다. 지형, 적 배치, 지역 오브젝트, 로컬 조명처럼 스테이지마다 달라지는 데이터가 여기에 들어갑니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공통 씬 + 콘텐츠 씬 구조</text>
  <rect x="40" y="40" width="400" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Persistent Scene (유지)</text>
  <text x="70" y="84" font-family="sans-serif" font-size="11" fill="currentColor">플레이어 캐릭터</text>
  <text x="70" y="100" font-family="sans-serif" font-size="11" fill="currentColor">카메라 시스템</text>
  <text x="70" y="116" font-family="sans-serif" font-size="11" fill="currentColor">게임 매니저</text>
  <text x="250" y="84" font-family="sans-serif" font-size="11" fill="currentColor">UI</text>
  <text x="250" y="100" font-family="sans-serif" font-size="11" fill="currentColor">조명 (글로벌)</text>
  <line x1="240" y1="160" x2="240" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="236,196 240,204 244,196" fill="currentColor"/>
  <polygon points="236,164 240,156 244,164" fill="currentColor"/>
  <text x="340" y="183" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Additive 로드 / 언로드</text>
  <rect x="40" y="210" width="400" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="240" y="232" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Content Scene (교체 대상)</text>
  <text x="70" y="254" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 지형</text>
  <text x="70" y="270" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 적 배치</text>
  <text x="270" y="254" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 오브젝트</text>
  <text x="270" y="270" font-family="sans-serif" font-size="11" fill="currentColor">스테이지별 조명 (로컬)</text>
  <text x="240" y="305" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점선 = 로드/언로드로 교체되는 씬</text>
  <rect x="40" y="335" width="400" height="78" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="240" y="355" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스테이지 전환 흐름</text>
  <text x="60" y="375" font-family="sans-serif" font-size="10" fill="currentColor">1. Content Scene (Stage 1) 언로드</text>
  <text x="60" y="391" font-family="sans-serif" font-size="10" fill="currentColor">2. UnloadUnusedAssets()</text>
  <text x="60" y="407" font-family="sans-serif" font-size="10" fill="currentColor">3. Content Scene (Stage 2) 비동기 로드</text>
  <text x="310" y="407" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 플레이어, UI는 유지됨</text>
</svg>
</div>

이 구조에서는 스테이지를 바꿀 때 콘텐츠 씬만 언로드하고 다음 콘텐츠 씬을 Additive로 로드합니다. 공통 씬은 계속 남아 있으므로 플레이어, 카메라, UI, 매니저를 다시 만들 필요가 없습니다. 전환 중에도 입력 상태나 UI 상태를 유지하기 쉽고, 공통 시스템의 초기화 비용도 반복해서 발생하지 않습니다.

DontDestroyOnLoad와 비교하면 수명 관리도 더 눈에 보입니다. DontDestroyOnLoad 씬은 Unity 내부에서 관리되므로 개발자가 씬 단위로 언로드할 수 없습니다. 그 안의 오브젝트를 정리하려면 개별적으로 `Destroy()`해야 합니다. 반면 공통 씬은 일반 씬이므로 로드 여부를 직접 제어할 수 있고, 필요하면 공통 씬 자체를 언로드해 그 안의 오브젝트를 한 번에 정리할 수 있습니다.

대신 경계는 분명히 해야 합니다. 특정 지역에서만 필요한 적, 지역 연출, 로컬 조명, 임시 오브젝트가 공통 씬에 들어가면 다시 전역 상주 객체가 됩니다. 공통 씬에는 여러 콘텐츠 씬을 지나도 계속 살아야 하는 것만 두고, 지역에 묶인 데이터는 콘텐츠 씬에 남기는 편이 좋습니다.

---

## 마무리

이번 글에서는 씬이 무엇으로 이루어지는지에서 출발해, 씬을 로드하고 유지하고 해제하는 과정을 메모리 사용과 함께 살펴보았습니다. 핵심은 다음과 같습니다.

- **동기 씬 로딩**은 로딩이 끝날 때까지 메인 스레드를 붙잡아 화면을 멈추게 합니다. 반면 **비동기 씬 로딩**은 파일 읽기와 역직렬화, 통합 작업을 여러 프레임과 스레드에 분산해 그 멈춤을 줄입니다.
- **`AsyncOperation`**의 `progress`는 0.9까지가 실제 로딩 구간이고 그 뒤가 활성화 구간이므로, 로딩 바로 표시할 때는 0.9를 100%로 환산합니다. **`allowSceneActivation`**을 false로 두면 활성화를 원하는 시점까지 미룰 수 있습니다.
- **Additive 모드**는 기존 씬을 둔 채 새 씬을 더해 여러 씬을 함께 올려 둡니다. UI와 게임 플레이, 환경을 역할별 씬으로 나누면 화면 전체를 한꺼번에 교체하지 않고 필요한 부분만 로드하거나 언로드할 수 있습니다.
- **`DontDestroyOnLoad`**는 씬이 바뀌어도 오브젝트를 살려 두지만, 그 오브젝트가 참조하는 에셋까지 함께 메모리에 남습니다. 따라서 전역으로 유지할 대상은 꼭 필요한 시스템으로 좁혀야 합니다.
- **씬 언로드**는 오브젝트를 파괴할 뿐, 그것이 참조하던 에셋을 곧바로 해제하지는 않습니다. Additive 씬을 내린 뒤 남은 에셋까지 해제하려면 `Resources.UnloadUnusedAssets()`를 직접 호출해야 합니다.
- **대규모 월드**는 월드를 격자 셀 단위 씬으로 나누고, 게임 내내 유지할 시스템을 담는 공통 씬과 지역별 콘텐츠 씬을 분리해 다룹니다. 플레이어 주변의 셀만 로드하도록 개수를 제한하면 메모리 상한을 예측하기 쉬워집니다.

결국 씬 관리는 메모리를 언제 확보하고 언제 해제할지 정하는 문제입니다. 어떤 에셋을 어느 시점에 로드하고 언로드할지, 전환 중 두 씬의 에셋이 겹치는 피크를 어떻게 낮출지가 메모리가 빠듯한 모바일에서 안정성을 좌우합니다.

<br>

이 글은 씬 단위의 로드와 해제를 다뤘습니다. 에셋 하나하나의 메모리 생명주기를 관리하는 AssetBundle과 Addressables의 로드·해제 패턴은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 이어집니다. 씬 안의 오브젝트가 어떤 구조로 연결되는지는 [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)에서 확인할 수 있습니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)
- [Unity 엔진 핵심 (3) - Unity 실행 순서](/dev/unity/UnityCore-3/)
- [Unity 엔진 핵심 (4) - Unity의 스레딩 모델](/dev/unity/UnityCore-4/)
- [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- **Unity 에셋 시스템 (3) - Scene Management** (현재 글)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
