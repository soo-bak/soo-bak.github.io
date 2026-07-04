---
layout: single
title: "Unity 에셋 시스템 (2) - Serialization과 Instantiation - soo:bak"
date: "2026-03-05 23:06:00 +0900"
description: Unity 직렬화 규칙, YAML 씬 파일 구조, 에셋 로딩 과정, Instantiate 내부 동작, Resources 폴더 문제를 설명합니다.
tags:
  - Unity
  - 에셋
  - Serialization
  - Instantiate
  - 모바일
---

## 임포트된 에셋이 저장되고 복제되는 방식

임포트는 한 번으로 끝나는 작업입니다. [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)에서 본 것처럼, 소스 에셋은 임포트를 거쳐 엔진이 직접 다루는 포맷으로 바뀌고 그 결과가 Library 폴더에 저장됩니다. PNG는 GPU 압축 텍스처가, FBX는 메쉬가 되고, 에셋끼리 서로를 가리키는 참조는 `.meta` 파일의 GUID로 이어집니다. 이렇게 한 번 만들어진 데이터는 소스를 고치지 않는 한 그대로 보관됩니다.

그런데 보관은 끝이 아니라 시작입니다. 같은 데이터가 게임이 실행되는 내내 디스크와 메모리 사이를 오갑니다. 씬을 저장하면 메모리에 올라와 있던 오브젝트가 디스크의 파일에 기록되고, 게임을 시작하면 그 파일이 런타임 오브젝트로 다시 구성됩니다. 실행 도중 `Instantiate`를 호출하면, 메모리에 있던 원본이 그대로 한 벌 더 복제됩니다.

세 경우는 방향이 제각각입니다. 메모리에서 디스크로, 디스크에서 메모리로, 메모리 안에서 다시 메모리로 향합니다. 그런데도 셋은 모두 **직렬화(Serialization)**라는 하나의 규칙 체계를 공유합니다. 직렬화는 오브젝트를 저장 가능한 형태로 바꾸는 처리이고, 그 규칙이 오브젝트의 어느 필드를 저장 대상에 넣고 어느 필드를 제외할지 결정합니다. 디스크에 기록될 때든 메모리로 복원될 때든 복제본으로 옮겨질 때든, 어떤 값이 함께 저장되고 어떤 값이 제외되는지는 모두 이 규칙을 따릅니다.

따라서 이 글은 직렬화 규칙을 맨 먼저 다룹니다. 어떤 필드가 저장되고 어떤 필드가 제외되는지 살펴본 뒤, 그렇게 직렬화된 씬 파일이 YAML로 참조를 적어 두는 구조, 디스크의 데이터가 런타임 메모리로 올라오는 로딩 과정, `Instantiate`가 복제하는 범위와 그대로 공유하는 대상, 끝으로 Resources 폴더의 구조적 한계를 차례로 다룹니다. 이 과정을 따라가고 나면, 왜 `public`으로 선언한 필드가 Inspector에 보이지 않을 때가 있는지, 왜 저장한 값이 다음 실행에서 사라지는지, 왜 프리팹 하나를 불렀을 뿐인데 메모리가 크게 늘어나는지를 설명할 수 있습니다.

---

## 직렬화(Serialization) 개요

오브젝트를 저장한다는 것은 메모리 배치를 그대로 복사한다는 뜻이 아닙니다. 파일에 남겨야 하는 것은 현재 실행에서의 위치가 아니라, 나중에 같은 상태를 다시 만들 수 있는 정보입니다. `Transform.position`의 숫자 값은 그대로 기록할 수 있지만, `MeshRenderer.material`처럼 다른 오브젝트를 가리키는 참조는 메모리 주소 그대로 저장할 수 없습니다.

메모리 주소는 실행할 때마다 다시 배정됩니다. 이번 실행에서 어떤 `Material`이 있던 주소를 파일에 적어 두어도, 다음 실행에서 그 주소가 같은 대상을 가리킨다는 보장은 없습니다. 따라서 참조는 주소가 아니라 다시 찾을 수 있는 식별 정보로 바꾸어 기록해야 합니다.

이처럼 오브젝트의 값을 정해진 형식으로 쓰고, 참조를 주소와 분리된 식별 정보로 바꾸어 연속된 바이트로 만드는 과정이 **직렬화(Serialization)**입니다. 직렬화 결과는 특정 실행의 메모리 배치에 묶이지 않는 데이터이며, 이런 연속된 바이트 데이터를 **바이트 스트림(byte stream)**이라고 합니다.

저장된 바이트 스트림을 다시 사용하려면 Unity는 데이터를 읽어 런타임 오브젝트를 만들고, 타입과 필드 정보에 맞춰 값을 채운 뒤 직렬화할 때 남겨 둔 식별 정보로 참조 대상을 다시 연결합니다. 이렇게 저장된 데이터를 읽어 오브젝트 상태를 복원하는 과정이 **역직렬화(Deserialization)**입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="270" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">직렬화와 역직렬화</text>
  <!-- Left box: Object (Memory) -->
  <rect x="10" y="34" width="210" height="190" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="115" y="54" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">오브젝트 (메모리)</text>
  <line x1="22" y1="62" x2="208" y2="62" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="28" y="82" font-size="11" font-weight="bold" font-family="sans-serif">Transform</text>
  <text fill="currentColor" x="40" y="100" font-size="10" font-family="sans-serif" opacity="0.7">position:</text>
  <text fill="currentColor" x="56" y="116" font-size="10" font-family="sans-serif" opacity="0.7">x = 1.0</text>
  <text fill="currentColor" x="56" y="132" font-size="10" font-family="sans-serif" opacity="0.7">y = 2.0</text>
  <text fill="currentColor" x="56" y="148" font-size="10" font-family="sans-serif" opacity="0.7">z = 0.0</text>
  <text fill="currentColor" x="28" y="170" font-size="11" font-weight="bold" font-family="sans-serif">MeshRenderer</text>
  <text fill="currentColor" x="40" y="188" font-size="10" font-family="sans-serif" opacity="0.7">material: ref</text>
  <!-- Right box: Byte stream (Disk) -->
  <rect x="320" y="34" width="210" height="190" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="425" y="54" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">바이트 스트림 (디스크)</text>
  <line x1="332" y1="62" x2="518" y2="62" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="340" y="82" font-size="10" font-family="monospace" opacity="0.7">0A 3F 00 00 ...</text>
  <text fill="currentColor" x="340" y="100" font-size="10" font-family="monospace" opacity="0.7">80 3F 00 00 ...</text>
  <text fill="currentColor" x="340" y="118" font-size="10" font-family="monospace" opacity="0.7">00 00 00 00 ...</text>
  <text fill="currentColor" x="340" y="136" font-size="10" font-family="monospace" opacity="0.7">00 40 00 00 ...</text>
  <text fill="currentColor" x="340" y="154" font-size="10" font-family="monospace" opacity="0.7">...</text>
  <!-- Forward arrow: Serialization (top) -->
  <line x1="220" y1="110" x2="310" y2="110" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="316,110 308,106 308,114" fill="currentColor"/>
  <text fill="currentColor" x="268" y="103" text-anchor="middle" font-size="10" font-family="sans-serif">직렬화</text>
  <!-- Return arrow: Deserialization (bottom, curved path) -->
  <path d="M 425 224 L 425 256 Q 425 266 415 266 L 125 266 Q 115 266 115 256 L 115 224" stroke="currentColor" stroke-width="1.5" fill="none"/>
  <polygon points="115,224 111,232 119,232" fill="currentColor"/>
  <text fill="currentColor" x="270" y="260" text-anchor="middle" font-size="10" font-family="sans-serif">역직렬화</text>
</svg>
</div>

<br>

Unity는 이 바이트 스트림을 프로젝트 파일로 저장합니다. 씬과 프리팹은 각각 `.unity`, `.prefab` 파일로 기록되고, ScriptableObject와 프로젝트 설정은 `.asset` 파일에 직렬화됩니다. 파일에 남는 것은 현재 실행의 메모리 주소가 아니라 값과 참조 식별 정보이므로, 에디터를 닫아 메모리가 비워진 뒤에도 데이터는 디스크에 남습니다.

이처럼 프로그램 실행이 끝난 뒤에도 데이터가 보존되는 성질을 **영속성(Persistence)**이라고 합니다. 씬을 다시 열면 Unity는 `.unity` 파일을 읽어 역직렬화하고, 저장해 둔 값과 참조 식별 정보를 바탕으로 GameObject와 Component를 메모리에 복원합니다.

직렬화 규칙은 디스크에 저장할 때만 적용되는 것이 아닙니다. 실행 중에 `Instantiate`로 오브젝트를 복제할 때도 Unity는 같은 규칙을 따라, 직렬화 대상인 필드의 값만 새 오브젝트로 옮깁니다. 따라서 직렬화에서 빠진 필드는 파일에 기록되지 않는 것은 물론, 복제본에도 그 값이 옮겨지지 않아 기본값으로 남습니다.

---

## Unity의 직렬화 규칙

직렬화 기능 자체는 C#에도 표준으로 들어 있어, `BinaryFormatter` 같은 .NET 클래스가 객체를 저장 가능한 형태로 바꿉니다. 하지만 Unity는 이 기능을 쓰지 않고 자체 직렬화를 구현합니다. 
Inspector 표시나 씬·프리팹 저장처럼, .NET 표준 직렬화 방식이 다루지 못하는 부분까지 처리해야 하기 때문입니다. 따라서 어떤 필드가 저장되는지는 Unity의 규칙을 알아야 예측할 수 있습니다.

이 규칙은 필드의 접근 제한자와 어트리뷰트를 기준으로 삼습니다. 접근 제한자는 외부 코드가 필드에 접근할 수 있는지(`public`) 없는지(`private`)를 정하는 키워드이고, 어트리뷰트는 `[SerializeField]`나 `[NonSerialized]`처럼 대괄호 안에 적어 필드의 동작을 지정하는 표식입니다. Unity는 이 둘을 근거로 직렬화할 필드를 결정하며, 그 결과에 따라 디스크에 저장되는 데이터와 Inspector에 표시되는 필드가 달라집니다.

### 자동 직렬화되는 필드

어떤 필드가 직렬화되는지는 우선 접근 제한자로 정해집니다. `public` 필드는 어트리뷰트를 따로 붙이지 않아도 Unity가 자동으로 직렬화하고, 아무 표식이 없는 `private` 필드는 직렬화 대상에서 제외됩니다. 접근 제한자가 이렇게 기본 동작을 정하고 나면, 어트리뷰트는 그 기본 동작을 바꾸려 할 때 덧붙이는 표식입니다. 접근 제한자와 어트리뷰트를 어떻게 조합하느냐에 따라 같은 필드라도 직렬화 여부가 달라집니다.

<br>

```csharp
// 직렬화 규칙 요약

// 자동 직렬화 (public 필드):
  public int health = 100;              // ← 직렬화됨
  public string playerName;             // ← 직렬화됨
  public float speed = 5f;              // ← 직렬화됨

// 명시적 직렬화 (private + 어트리뷰트):
  [SerializeField]
  private int secretValue;              // ← 직렬화됨 (Inspector에 표시)

// 직렬화 제외:
  [NonSerialized]
  public int tempValue;                 // ← 직렬화 안 됨

  [HideInInspector]
  public int hiddenValue;               // ← 직렬화되지만 Inspector에 숨김

  private int internalValue;            // ← 직렬화 안 됨 (기본 동작)
  static int sharedValue;               // ← 직렬화 안 됨
  const int MAX = 100;                  // ← 직렬화 안 됨
  readonly int fixedValue = 10;         // ← 직렬화 안 됨
```

<br>

기본적으로 직렬화되지 않는 `private` 필드도 `[SerializeField]`를 붙이면 저장 대상이 됩니다. 반대로 자동으로 직렬화되는 `public` 필드도 `[NonSerialized]`를 붙이면 저장 대상에서 빠집니다.

따라서 Inspector에서 값을 편집해야 한다는 이유만으로 필드를 `public`으로 열 필요는 없습니다. `public`은 Unity가 값을 저장한다는 뜻일 뿐 아니라, 다른 스크립트가 그 필드에 직접 접근할 수 있다는 뜻이기도 합니다. 외부 코드가 객체의 내부 값을 마음대로 바꾸면, 그 객체가 지켜야 할 상태 규칙이 쉽게 깨집니다. 이런 상황을 막기 위한 설계 원칙이 **캡슐화(Encapsulation)**입니다.

값은 저장하고 Inspector에서는 편집하게 하되, 코드에서는 외부에 공개하고 싶지 않다면 `[SerializeField] private`을 사용합니다. `[SerializeField]`는 직렬화 대상만 바꿀 뿐 접근 제한자는 건드리지 않으므로, 필드는 `private`인 채로 Inspector에 표시됩니다.

직렬화 여부와 Inspector 표시 여부는 별개입니다. 직렬화 대상인 필드에 `[HideInInspector]`를 붙이면 값은 씬이나 프리팹에 저장되지만, Inspector 창에는 보이지 않습니다. 코드가 계산해서 채우는 값처럼 저장은 필요하지만 사람이 직접 편집하면 안 되는 필드에 사용할 수 있습니다.

코드 예시에 남은 `static`, `const`, `readonly` 필드는 접근 제한자를 바꾸거나 어트리뷰트를 붙여도 직렬화되지 않습니다. Unity가 파일로 저장하는 값은 컴포넌트나 ScriptableObject의 개별 **인스턴스(Instance)**에 속한 상태입니다. 같은 컴포넌트가 두 오브젝트에 붙어 있어도 둘은 서로 다른 인스턴스이므로, `public int health`도 한쪽은 100, 다른 쪽은 30처럼 인스턴스마다 다른 값으로 저장됩니다.

`static` 필드는 인스턴스가 아니라 타입에 속해, 컴포넌트를 몇 개 생성하든 모두가 하나의 값을 공유합니다. `const`도 컴파일 시점에 코드에 고정되는 상수이므로 특정 인스턴스의 상태가 아닙니다. 따라서 두 필드에는 인스턴스마다 저장할 상태가 없습니다.

`readonly` 필드는 다른 이유로 제외됩니다. 이 필드는 한 번 값이 정해지면 다시 바꿀 수 없다는 뜻입니다. Unity 직렬화는 값을 파일에 적어 두는 데서 끝나지 않고, 나중에 씬이나 프리팹을 열 때 그 값을 필드에 다시 넣어야 합니다. 예를 들어 어떤 필드 값이 30으로 저장되어 있었다면, 로드할 때 Unity는 컴포넌트를 만든 뒤 그 필드에 30을 대입해야 합니다. 일반 필드는 이 과정이 가능하지만, `readonly` 필드는 이미 초기화가 끝난 뒤라 다시 대입할 수 없습니다. 따라서 Unity는 `readonly` 필드를 처음부터 직렬화 대상에 넣지 않습니다.

### 직렬화 가능한 타입

필드를 `public`으로 선언하든 `[SerializeField]`를 붙이든, 그 필드의 **타입(Type)**이 직렬화를 지원하지 않으면 값은 저장되지 않습니다. 직렬화를 지원하는 타입과 그렇지 않은 타입은 아래 그림과 같이 나뉩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 제목 -->
  <text x="230" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">직렬화 가능한 타입</text>
  <!-- 지원 영역 -->
  <rect x="10" y="36" width="440" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">지원</text>
  <text x="36" y="82" font-family="sans-serif" font-size="11" fill="currentColor">기본형</text>
  <text x="130" y="82" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">int, float, bool, string, char, byte 등</text>
  <text x="36" y="102" font-family="sans-serif" font-size="11" fill="currentColor">Unity 구조체</text>
  <text x="130" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Vector3, Quaternion, Color, Rect 등</text>
  <text x="36" y="122" font-family="sans-serif" font-size="11" fill="currentColor">Unity 오브젝트 참조</text>
  <text x="170" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GameObject, Transform, Texture 등</text>
  <text x="36" y="142" font-family="sans-serif" font-size="11" fill="currentColor">enum</text>
  <text x="36" y="162" font-family="sans-serif" font-size="11" fill="currentColor">배열</text>
  <text x="130" y="162" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">int[], string[] 등</text>
  <text x="36" y="182" font-family="sans-serif" font-size="11" fill="currentColor">List&lt;T&gt;</text>
  <text x="130" y="182" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">List&lt;int&gt;, List&lt;string&gt; 등</text>
  <text x="36" y="202" font-family="sans-serif" font-size="11" fill="currentColor">[Serializable] 클래스/구조체</text>
  <text x="230" y="202" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(커스텀)</text>
  <!-- 구분선 -->
  <line x1="10" y1="236" x2="450" y2="236" stroke="currentColor" stroke-width="1.5"/>
  <!-- 미지원 영역 -->
  <rect x="10" y="236" width="440" height="176" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="260" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">미지원</text>
  <text x="36" y="284" font-family="sans-serif" font-size="11" fill="currentColor">Dictionary&lt;K,V&gt;</text>
  <text x="36" y="304" font-family="sans-serif" font-size="11" fill="currentColor">인터페이스 타입 필드</text>
  <text x="36" y="324" font-family="sans-serif" font-size="11" fill="currentColor">추상 클래스 타입 필드</text>
  <text x="36" y="344" font-family="sans-serif" font-size="11" fill="currentColor">다차원 배열</text>
  <text x="130" y="344" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(int[,])</text>
  <text x="36" y="364" font-family="sans-serif" font-size="11" fill="currentColor">중첩된 제네릭</text>
  <text x="140" y="364" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(List&lt;List&lt;int&gt;&gt;)</text>
  <text x="36" y="384" font-family="sans-serif" font-size="11" fill="currentColor">프로퍼티</text>
  <text x="130" y="384" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(getter/setter)</text>
</svg>
</div>

<br>

지원 목록 끝의 커스텀 클래스와 구조체는 직접 정의한 타입이라 기본적으로는 직렬화 대상 밖에 있습니다. 타입 선언에 `[Serializable]` 어트리뷰트를 붙이면 지원 대상이 되고, 그 안의 필드들도 접근 제한자와 어트리뷰트 규칙을 그대로 따라 저장됩니다.

미지원 타입을 선언해도 C# 컴파일 오류가 발생하는 것은 아닙니다. `public Dictionary<string, int> inventory;`는 정상적인 C# 필드이므로 코드는 컴파일됩니다. 다만 `Dictionary`는 Unity 기본 직렬화의 지원 대상이 아니므로 Inspector에는 표시되지 않고, 씬이나 프리팹을 저장해도 그 안의 키와 값은 기록되지 않습니다.

Dictionary 값을 저장해야 한다면 Unity가 지원하는 형태로 바꿔 두어야 합니다. 이때 사용하는 인터페이스가 `ISerializationCallbackReceiver`입니다. 저장 직전 `OnBeforeSerialize()`에서 Dictionary의 키와 값을 각각 List로 옮기면, Unity는 `List<TKey>`와 `List<TValue>`를 일반 필드처럼 저장할 수 있습니다. 다시 불러온 뒤에는 `OnAfterDeserialize()`에서 두 List를 순서대로 읽어 Dictionary를 다시 만듭니다.

<br>

### [SerializeReference]로 다형성 지원

앞에서 인터페이스 타입 필드와 추상 클래스 타입 필드는 기본 직렬화 대상이 아니라고 했습니다. 이유는 단순합니다. Unity의 기본 직렬화는 필드의 **선언 타입**을 기준으로 값을 저장하고, 다시 불러올 때도 그 선언 타입의 인스턴스를 만들려고 합니다.

이 방식은 상속 관계가 들어오면 한계가 드러납니다. C# 코드에서는 부모 타입 변수에 자식 객체를 넣을 수 있지만, 기본 직렬화는 그 객체의 실제 타입까지 함께 보존하지 않습니다. 먼저 예시를 보겠습니다.

<br>

```csharp
[Serializable] class BaseEffect { public int duration; }
[Serializable] class FireEffect : BaseEffect { public int damage; }

public class EffectHolder : MonoBehaviour
{
    // 기본 직렬화: 선언 타입(BaseEffect) 기준
    public BaseEffect inlineEffect;

    // SerializeReference: 실제 타입(FireEffect) 정보까지 저장
    [SerializeReference]
    public BaseEffect referencedEffect;
}

// 두 필드에 FireEffect 인스턴스를 넣었다고 가정
// inlineEffect     → BaseEffect의 duration만 저장
// referencedEffect → FireEffect 타입 정보와 damage까지 저장
```

<br>

`inlineEffect`는 선언 타입이 `BaseEffect`입니다. 여기에 `FireEffect` 인스턴스를 넣어도 C# 실행 중에는 문제가 없지만, Unity가 저장할 때는 `BaseEffect`에 정의된 `duration`만 봅니다. `FireEffect`에만 있는 `damage`는 선언 타입에 없는 필드이므로 저장 대상에서 빠지고, 다시 불러올 때도 `BaseEffect`로 복원됩니다.

반면 `referencedEffect`에는 `[SerializeReference]`가 붙어 있습니다. 이 경우 Unity는 필드 값을 인라인으로 복사하는 대신, 관리 참조(Managed Reference)로 저장합니다. 값과 함께 실제 런타임 타입도 기록하므로, 다시 불러올 때 `FireEffect` 인스턴스를 만들고 `damage`까지 복원할 수 있습니다.

이 차이가 `[SerializeReference]`가 다형성을 지원하는 방식입니다. 부모 타입, 인터페이스, 추상 클래스처럼 선언 타입만으로는 실제 객체를 만들기 어려운 필드라도, 저장된 실제 타입이 구체 클래스라면 그 타입으로 복원할 수 있습니다.

다만 `[SerializeReference]`는 모든 참조에 쓰는 범용 해결책은 아닙니다. 필드에 들어가는 값은 `UnityEngine.Object`를 상속하지 않는 순수 C# 클래스의 인스턴스여야 합니다. `MonoBehaviour`나 `ScriptableObject` 같은 Unity 오브젝트는 엔진이 에셋 참조와 인스턴스 ID로 따로 관리하므로, 이런 타입은 일반 Unity 오브젝트 참조로 다루어야 합니다. 또한 관리 참조를 저장하는 기능이므로 값 타입인 `struct`에는 사용할 수 없습니다.

타입 이름 변경에도 주의해야 합니다. `[SerializeReference]`는 실제 타입을 네임스페이스와 클래스 이름, 어셈블리 이름으로 기록합니다. 이후 클래스 이름이나 네임스페이스를 바꾸면 파일에 남아 있는 타입 문자열과 현재 코드의 타입 이름이 맞지 않아 기존 데이터를 역직렬화하지 못할 수 있습니다. `MovedFrom` 어트리뷰트로 이전 이름과 새 이름을 연결해 완화할 수 있지만, 프리팹 오버라이드가 얽힌 인스턴스에서는 이 연결이 항상 원하는 대로 적용되지 않을 수 있습니다.

마지막으로 null과 공유 참조 처리도 기본 직렬화와 다릅니다. 기본 직렬화는 커스텀 클래스 필드의 null을 빈 인스턴스로 대체하고, 같은 객체를 가리키던 두 필드도 각각 별도의 값처럼 저장합니다. `[SerializeReference]`는 null을 null 그대로 유지하고, 여러 필드가 같은 객체를 가리키는 공유 참조 구조도 보존합니다. 다형성뿐 아니라 객체 그래프의 형태를 유지해야 할 때도 이 차이가 중요합니다.

### ScriptableObject: 데이터 공유와 중복 제거

기본 직렬화가 필드 값을 인스턴스 안에 저장한다는 점은 게임 데이터 구조에도 영향을 줍니다. 예를 들어 모든 적이 같은 체력, 이동 속도, 공격력을 쓴다고 해도 이 값을 `MonoBehaviour` 필드에 직접 넣으면 각 적 컴포넌트가 자기 값을 따로 갖습니다. 씬에 직접 배치된 오브젝트라면 같은 숫자가 씬 파일에도 반복해서 기록됩니다.

이런 값이 개별 인스턴스의 상태가 아니라 공통 설계 데이터라면, 오브젝트마다 복사해 둘 필요가 없습니다. 한 곳에 에셋으로 만들어 두고 여러 오브젝트가 그 에셋을 참조하게 만들면 됩니다. 이때 사용하는 타입이 **ScriptableObject**입니다.

ScriptableObject는 GameObject에 붙는 컴포넌트가 아니라 독립적인 Unity 오브젝트입니다. 보통 `.asset` 파일로 저장해 두고, `MonoBehaviour` 필드에서는 그 에셋을 참조합니다. 그러면 각 적 오브젝트에는 `hp`, `speed`, `damage` 값 자체가 반복 저장되는 대신, 같은 `EnemyStats` 에셋을 가리키는 참조만 남습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="280" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">반복 데이터와 ScriptableObject 참조</text>

  <!-- === Top section: MonoBehaviour에 직접 데이터를 넣는 경우 === -->
  <text fill="currentColor" x="280" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">값을 각 인스턴스에 둔 경우</text>

  <!-- Enemy(1) box -->
  <rect x="20" y="64" width="150" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="95" y="84" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(1)</text>
  <line x1="32" y1="91" x2="158" y2="91" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="38" y="110" font-size="11" font-family="sans-serif">hp: 100</text>
  <text fill="currentColor" x="38" y="130" font-size="11" font-family="sans-serif">speed: 5</text>
  <text fill="currentColor" x="38" y="150" font-size="11" font-family="sans-serif">damage: 10</text>

  <!-- Enemy(2) box -->
  <rect x="205" y="64" width="150" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="280" y="84" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(2)</text>
  <line x1="217" y1="91" x2="343" y2="91" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="223" y="110" font-size="11" font-family="sans-serif">hp: 100</text>
  <text fill="currentColor" x="223" y="130" font-size="11" font-family="sans-serif">speed: 5</text>
  <text fill="currentColor" x="223" y="150" font-size="11" font-family="sans-serif">damage: 10</text>

  <!-- Enemy(3) box -->
  <rect x="390" y="64" width="150" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="465" y="84" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(3)</text>
  <line x1="402" y1="91" x2="528" y2="91" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="408" y="110" font-size="11" font-family="sans-serif">hp: 100</text>
  <text fill="currentColor" x="408" y="130" font-size="11" font-family="sans-serif">speed: 5</text>
  <text fill="currentColor" x="408" y="150" font-size="11" font-family="sans-serif">damage: 10</text>

  <!-- Conclusion arrow: top section -->
  <text fill="currentColor" x="280" y="198" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">→ 같은 설계 값이 인스턴스마다 반복 저장됨</text>

  <!-- === Divider === -->
  <line x1="40" y1="220" x2="520" y2="220" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- === Bottom section: ScriptableObject로 공유하는 경우 === -->
  <text fill="currentColor" x="280" y="250" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">ScriptableObject 에셋을 참조하는 경우</text>

  <!-- Enemy(1) ref box -->
  <rect x="20" y="264" width="150" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="95" y="284" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(1)</text>
  <line x1="32" y1="291" x2="158" y2="291" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="38" y="312" font-size="11" font-family="sans-serif">stats: ref →</text>

  <!-- Enemy(2) ref box -->
  <rect x="205" y="264" width="150" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="280" y="284" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(2)</text>
  <line x1="217" y1="291" x2="343" y2="291" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="223" y="312" font-size="11" font-family="sans-serif">stats: ref →</text>

  <!-- Enemy(3) ref box -->
  <rect x="390" y="264" width="150" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="465" y="284" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Enemy(3)</text>
  <line x1="402" y1="291" x2="528" y2="291" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="408" y="312" font-size="11" font-family="sans-serif">stats: ref →</text>

  <!-- Reference arrows from each Enemy to SO -->
  <line x1="95" y1="334" x2="280" y2="390" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="280" y1="334" x2="280" y2="390" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="465" y1="334" x2="280" y2="390" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- Arrowhead -->
  <polygon points="280,392 275,382 285,382" fill="currentColor" opacity="0.4"/>

  <!-- EnemyStats (SO) box -->
  <rect x="180" y="394" width="200" height="100" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="280" y="416" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">EnemyStats (SO)</text>
  <line x1="192" y1="423" x2="368" y2="423" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="200" y="443" font-size="11" font-family="sans-serif">hp: 100</text>
  <text fill="currentColor" x="200" y="463" font-size="11" font-family="sans-serif">speed: 5</text>
  <text fill="currentColor" x="200" y="483" font-size="11" font-family="sans-serif">damage: 10</text>

  <!-- Conclusion arrow: bottom section -->
  <text fill="currentColor" x="280" y="514" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">→ 공통 데이터는 한 에셋에 두고 참조만 공유</text>
</svg>
</div>

<br>

그림 아래쪽처럼 데이터를 ScriptableObject로 옮기면, 각 오브젝트의 필드에는 값이 아니라 Unity 오브젝트 참조가 저장됩니다. 이 참조는 앞에서 본 Unity 오브젝트 참조 직렬화 규칙을 따르므로, 여러 오브젝트가 같은 `.asset` 파일을 가리킬 수 있습니다. 오브젝트가 100개여도 공통 스탯 값은 `EnemyStats` 에셋 한 곳에 있고, 각 오브젝트는 그 에셋을 찾아갈 참조만 갖습니다.

이 구조는 반복되는 읽기 전용 데이터에 특히 잘 맞습니다. 적 스탯, 아이템 정의, 스킬 설정, 대화 데이터처럼 여러 인스턴스가 같은 값을 읽어야 하는 경우에는 ScriptableObject로 빼면 중복 저장을 줄이고 수정 지점도 하나로 모을 수 있습니다. 값 하나를 조정하면 같은 에셋을 참조하는 오브젝트들이 모두 같은 변경을 보게 됩니다.

반대로 개별 인스턴스마다 달라져야 하는 런타임 상태를 ScriptableObject에 넣으면 문제가 됩니다. 한 적의 현재 체력처럼 객체마다 따로 변해야 하는 값이 ScriptableObject에 있으면, 같은 에셋을 참조하는 다른 적도 같은 값을 보게 됩니다. 따라서 ScriptableObject에는 기본값과 설정을 두고, 전투 중 변하는 현재 상태는 MonoBehaviour 인스턴스나 별도 런타임 데이터에 복사해 관리하는 편이 안전합니다.

런타임에 ScriptableObject 값을 직접 바꿀 때도 주의해야 합니다. 빌드에서는 바뀐 값이 같은 실행 세션 동안 모든 참조에 반영되지만, 앱을 다시 실행하면 직렬화된 원래 값으로 돌아갑니다. 에디터에서는 플레이 모드 중 수정한 에셋 인스턴스가 그대로 남아, 변경이 의도치 않게 `.asset` 파일에 저장될 수 있습니다. 그래서 ScriptableObject는 기본적으로 공유 설정 데이터로 보고, 플레이 중 상태 저장소처럼 쓰지 않는 편이 좋습니다.

---

## YAML 씬 파일 구조

Unity가 씬(`.unity`)과 프리팹(`.prefab`)을 저장할 때 기록하는 것은 GameObject, Component, 필드 값, 참조 관계입니다. 이 데이터는 바이너리로도 저장할 수 있지만, 텍스트로 저장하면 파일 안에서 실제 구조를 직접 확인할 수 있습니다. Unity가 이 텍스트 저장에 사용하는 형식이 **YAML**입니다.

YAML은 들여쓰기와 키-값 구조로 데이터를 표현하는 직렬화 포맷입니다. Unity 파일에서는 하나의 오브젝트가 하나의 블록으로 기록되고, 그 안에 컴포넌트 필드와 다른 오브젝트를 가리키는 참조 정보가 들어갑니다. 텍스트 에디터로 열어 보면 어떤 GameObject가 어떤 Component를 갖는지, 어떤 필드가 어떤 에셋이나 오브젝트를 참조하는지 따라갈 수 있습니다.

이 방식은 프로젝트 설정(Edit > Project Settings > Editor)의 **Asset Serialization Mode**가 **Force Text**일 때 적용됩니다. Binary 모드로 바꾸면 같은 데이터가 사람이 읽기 어려운 바이너리로 저장됩니다. 버전 관리에서 변경 이력을 추적하고, 병합 충돌을 사람이 직접 확인해야 하는 프로젝트라면 Force Text를 유지하는 편이 일반적입니다.

YAML 구조를 읽을 줄 알면 참조가 끊어진 이유를 파일에서 확인하거나, 씬 병합 충돌이 났을 때 어느 오브젝트 블록이 충돌했는지 판단할 수 있습니다. 다음 절부터는 이 파일 안에서 오브젝트를 식별하는 `fileID`와, 외부 에셋을 가리키는 `guid`가 어떻게 기록되는지 살펴보겠습니다.

### fileID와 오브젝트 식별

씬 파일 안에는 GameObject와 Component가 각각 별도의 오브젝트 블록으로 저장됩니다. Unity는 이 블록을 구분하기 위해 **fileID**를 붙입니다. fileID는 프로젝트 전체에서 통하는 ID가 아니라, 해당 YAML 파일 안에서만 대상을 식별하는 번호입니다.

각 블록은 `--- !u!<classID> &<fileID>` 형식의 헤더로 시작합니다. `!u!` 뒤의 숫자는 **classID**로, Unity가 내부 타입마다 정해 둔 번호입니다. 예를 들어 1은 GameObject, 4는 Transform, 23은 MeshRenderer를 뜻합니다. `&` 뒤의 숫자가 fileID이며, 같은 파일 안에서 그 오브젝트를 가리킬 때 사용됩니다.

<br>

```yaml
# .unity 파일의 YAML 구조 (간략화)

--- !u!1 &100000                    # classID 1 = GameObject
GameObject:
  m_Name: Player
  m_Component:
    - component: {fileID: 100001}   # 같은 파일 안의 Transform
    - component: {fileID: 100002}   # 같은 파일 안의 MeshRenderer

--- !u!4 &100001                    # classID 4 = Transform
Transform:
  m_LocalPosition: {x: 0, y: 1, z: 0}
  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}
  m_GameObject: {fileID: 100000}    # 소속 GameObject

--- !u!23 &100002                   # classID 23 = MeshRenderer
MeshRenderer:
  m_Materials:
    - {fileID: 2100000, guid: abc123..., type: 2}
      # 외부 머티리얼 에셋 참조
```

<br>

참조 방식은 대상이 같은 파일 안에 있는지, 다른 에셋 파일에 있는지에 따라 달라집니다.

같은 `.unity` 파일 안의 오브젝트를 가리킬 때는 fileID만 적습니다. 위 예시에서 GameObject의 `m_Component`가 `{fileID: 100001}`과 `{fileID: 100002}`를 가리키는 부분이 여기에 해당합니다. Transform과 MeshRenderer가 같은 씬 파일 안에 있으므로, Unity는 파일 내부 번호만으로 대상을 찾을 수 있습니다.

다른 파일에 있는 에셋을 가리킬 때는 fileID만으로 부족합니다. 머티리얼, 텍스처, 프리팹, FBX는 각각 별도 에셋 파일에 있으므로, Unity는 어느 파일을 열어야 하는지를 나타내는 `guid`와 그 파일 안의 어떤 오브젝트를 참조하는지를 나타내는 `fileID`를 함께 기록합니다. 이때 `guid`는 대상 에셋의 `.meta` 파일에 저장된 식별자입니다.

`guid`와 `fileID`를 함께 쓰는 이유는 에셋 파일 하나가 여러 서브 오브젝트를 가질 수 있기 때문입니다. 예를 들어 FBX 파일 하나 안에도 메쉬, 애니메이션 클립, 내장 머티리얼이 함께 들어갈 수 있습니다. `guid`만 있으면 FBX 파일까지는 찾을 수 있지만, 그 안의 어느 서브 오브젝트를 참조하는지는 알 수 없습니다.

참조에 함께 기록되는 `type`은 Unity가 참조 파일의 종류를 해석할 때 사용하는 값입니다. YAML을 읽으며 참조를 추적할 때 핵심은 `guid`와 `fileID`입니다. 먼저 `guid`로 에셋 파일을 찾고, 그 파일 안에서 `fileID`에 해당하는 오브젝트를 찾는 흐름으로 보면 됩니다.

### .meta 파일과 GUID의 관계

씬 파일에 기록된 `guid`는 에셋의 경로가 아니라 에셋을 식별하는 값입니다. Unity는 에셋을 임포트할 때 GUID를 만들고, 그 값을 에셋 옆의 `.meta` 파일에 저장합니다. 따라서 어떤 GUID가 어떤 파일을 가리키는지는 에셋 파일 자체가 아니라 `.meta` 파일을 통해 확인됩니다.

> `.meta` 파일이 에셋마다 GUID를 보관하는 구조는 [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)에서 자세히 다룹니다.

앞 절의 머티리얼 참조를 다시 보면, 씬 파일에는 머티리얼의 경로가 직접 적히지 않습니다. 대신 `guid`와 `fileID`가 기록되고, Unity는 이 GUID를 가진 `.meta` 파일을 찾아 실제 에셋 파일로 연결합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 660 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="330" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">참조 체인</text>
  <!-- Column labels -->
  <text fill="currentColor" x="105" y="40" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">씬 파일 (.unity)</text>
  <text fill="currentColor" x="330" y="40" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">.meta 파일</text>
  <text fill="currentColor" x="555" y="40" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">에셋 파일</text>
  <!-- Left box: Scene file -->
  <rect x="10" y="50" width="190" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="24" y="72" font-size="11" font-weight="bold" font-family="sans-serif">MeshRenderer</text>
  <line x1="22" y1="80" x2="188" y2="80" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="34" y="98" font-size="10" font-family="sans-serif" opacity="0.7">material:</text>
  <text fill="currentColor" x="46" y="116" font-size="10" font-family="monospace" opacity="0.7">guid: abc123...</text>
  <text fill="currentColor" x="46" y="134" font-size="10" font-family="monospace" opacity="0.7">fileID: 2100000</text>
  <!-- Arrow: Scene → .meta -->
  <line x1="200" y1="105" x2="232" y2="105" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="238,105 230,101 230,109" fill="currentColor"/>
  <!-- Center box: .meta file -->
  <rect x="240" y="50" width="180" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="254" y="72" font-size="11" font-weight="bold" font-family="sans-serif">material.mat.meta</text>
  <line x1="252" y1="80" x2="408" y2="80" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="264" y="106" font-size="10" font-family="monospace" opacity="0.7">guid: abc123...</text>
  <!-- Arrow: .meta → Asset -->
  <line x1="420" y1="105" x2="452" y2="105" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="458,105 450,101 450,109" fill="currentColor"/>
  <!-- Right box: Asset file -->
  <rect x="460" y="50" width="190" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="474" y="72" font-size="11" font-weight="bold" font-family="sans-serif">material.mat</text>
  <line x1="472" y1="80" x2="638" y2="80" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="555" y="108" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">(머티리얼 데이터)</text>
  <!-- Notes -->
  <text fill="currentColor" x="330" y="192" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">GUID가 유지되면 파일 이름이나 경로가 바뀌어도 참조 유지</text>
  <text fill="currentColor" x="330" y="210" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">.meta 파일 재생성 = GUID 변경 = 기존 참조 손실</text>
</svg>
</div>

<br>

Unity의 에셋 참조는 파일 경로가 아니라 GUID를 기준으로 이어집니다. 그래서 에셋의 이름이나 폴더 위치가 바뀌어도, 같은 `.meta` 파일이 유지되어 GUID가 변하지 않으면 씬과 프리팹의 참조는 그대로 살아 있습니다.

문제가 되는 경우는 `.meta` 파일이 사라지거나 새로 만들어질 때입니다. Unity가 새 `.meta` 파일을 만들면 새 GUID가 부여되고, 기존 씬과 프리팹에 기록된 GUID는 더 이상 그 에셋을 가리키지 못합니다. 이 상태가 Inspector에서 보이는 Missing 참조의 흔한 원인입니다.

따라서 `.meta` 파일은 에셋 파일과 같은 단위로 다뤄야 합니다. 버전 관리에는 에셋과 `.meta` 파일을 함께 포함하고, 이름 변경이나 이동은 가능한 한 Unity 에디터의 Project 창에서 처리합니다. 에디터 밖에서 옮겨야 한다면 소스 파일만 옮기지 말고 대응되는 `.meta` 파일까지 함께 옮겨야 합니다.

---

## 에셋 로딩 과정

지금까지 본 씬, 프리팹, `.meta` 파일은 디스크에 저장된 직렬화 데이터입니다. 이 데이터는 파일에 기록된 값일 뿐이라, 게임 실행 중에 곧바로 사용할 수 있는 Texture, Mesh, Material 같은 런타임 오브젝트는 아닙니다.

게임이 에셋을 사용하려면 먼저 파일에서 데이터를 읽고, 참조 관계를 따라 필요한 의존 에셋을 찾은 뒤, 타입과 필드 정보를 해석해 메모리 위의 오브젝트로 복원해야 합니다. 이 과정을 **에셋 로딩(Asset Loading)**이라고 합니다.

### 로딩의 기본 흐름

에셋을 메모리에 올리는 과정은 단순히 파일 하나를 읽는 작업이 아닙니다. Unity는 먼저 에셋 안에 어떤 오브젝트가 들어 있는지와 어떤 다른 에셋을 참조하는지 확인합니다. 그다음 필요한 의존 에셋을 준비하고, 직렬화된 값을 런타임 오브젝트로 복원한 뒤, 텍스처나 메쉬처럼 실제 사용에 필요한 데이터를 알맞은 메모리 영역에 배치합니다.

단순화하면 흐름은 다음 세 단계로 볼 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 590" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="210" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">에셋 로딩 과정</text>

  <!-- Step 1: Header reading -->
  <rect x="30" y="40" width="360" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="62" font-size="12" font-weight="bold" font-family="sans-serif">1. 메타데이터 읽기</text>
  <line x1="40" y1="70" x2="380" y2="70" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="44" y="90" font-size="10" font-family="sans-serif">에셋에 포함된 오브젝트와</text>
  <text fill="currentColor" x="44" y="106" font-size="10" font-family="sans-serif">외부 참조 목록을 확인</text>
  <text fill="currentColor" x="44" y="130" font-size="9" font-family="sans-serif" opacity="0.5">예: 머티리얼 → 텍스처, 셰이더 참조</text>

  <!-- Arrow 1→2 -->
  <line x1="210" y1="150" x2="210" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,186 205,176 215,176" fill="currentColor"/>

  <!-- Step 2: Dependency resolution & deserialization -->
  <rect x="30" y="190" width="360" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="212" font-size="12" font-weight="bold" font-family="sans-serif">2. 의존성 해결과 복원</text>
  <line x1="40" y1="220" x2="380" y2="220" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="44" y="240" font-size="10" font-family="sans-serif">아직 없는 참조 에셋을 함께 준비</text>
  <text fill="currentColor" x="44" y="264" font-size="10" font-family="sans-serif">직렬화된 값을 런타임 오브젝트로 복원</text>
  <text fill="currentColor" x="44" y="284" font-size="9" font-family="sans-serif" opacity="0.5">타입 확인 → 필드 값 적용 → 참조 연결</text>

  <!-- Arrow 2→3 -->
  <line x1="210" y1="310" x2="210" y2="340" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,346 205,336 215,336" fill="currentColor"/>

  <!-- Step 3: Memory placement -->
  <rect x="30" y="350" width="360" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="372" font-size="12" font-weight="bold" font-family="sans-serif">3. 런타임 리소스 준비</text>
  <line x1="40" y1="380" x2="380" y2="380" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Memory mapping items -->
  <text fill="currentColor" x="60" y="404" font-size="10" font-family="sans-serif">텍스처</text>
  <line x1="100" y1="400" x2="170" y2="400" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="174,400 168,397 168,403" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="180" y="404" font-size="10" font-family="sans-serif">GPU 리소스 *</text>

  <text fill="currentColor" x="60" y="428" font-size="10" font-family="sans-serif">메쉬 버퍼</text>
  <line x1="118" y1="424" x2="170" y2="424" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="174,424 168,421 168,427" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="180" y="428" font-size="10" font-family="sans-serif">GPU 리소스 *</text>

  <text fill="currentColor" x="60" y="452" font-size="10" font-family="sans-serif">C# 오브젝트 래퍼</text>
  <line x1="160" y1="448" x2="218" y2="448" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="222,448 216,445 216,451" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="228" y="452" font-size="10" font-family="sans-serif">관리 힙</text>

  <text fill="currentColor" x="60" y="476" font-size="10" font-family="sans-serif">네이티브 데이터</text>
  <line x1="148" y1="472" x2="218" y2="472" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="222,472 216,469 216,475" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="228" y="476" font-size="10" font-family="sans-serif">네이티브 메모리</text>

  <!-- Footnote separator -->
  <line x1="50" y1="498" x2="380" y2="498" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <!-- Platform notes -->
  <text fill="currentColor" x="60" y="518" font-size="9" font-family="sans-serif" opacity="0.5">* PC/콘솔: 별도 VRAM</text>
  <text fill="currentColor" x="64" y="534" font-size="9" font-family="sans-serif" opacity="0.5">모바일: CPU와 공유하는 통합 메모리</text>
</svg>
</div>

<br>

이 흐름에서 로딩 시간과 메모리에 크게 영향을 주는 부분은 의존성 해결입니다. 에셋 A가 B를 참조하고, B가 다시 C를 참조한다면 A를 로드하는 과정에서 B와 C도 함께 필요해집니다. 요청한 에셋은 하나여도 실제로 메모리에 올라오는 대상은 여러 개가 될 수 있습니다.

따라서 로딩 비용은 에셋 파일 하나의 크기만으로 결정되지 않습니다. 의존성 체인이 깊거나 한 에셋이 많은 대상을 참조할수록 읽어야 할 파일과 복원해야 할 오브젝트가 늘어납니다. 예를 들어 프리팹 하나가 머티리얼을 참조하고, 그 머티리얼이 텍스처 3장과 셰이더를 참조한다면 프리팹을 요청했을 뿐이어도 관련 에셋들이 함께 로드될 수 있습니다.

### 동기 로딩 vs 비동기 로딩

같은 에셋을 로드하더라도 호출 방식에 따라 프레임에 주는 영향은 달라집니다. **동기(Synchronous)** 로딩은 요청한 에셋이 준비될 때까지 호출 지점에서 기다립니다. 함수가 반환되는 순간 에셋을 바로 사용할 수 있다는 장점은 있지만, 메인 스레드에서 호출하면 로딩이 끝날 때까지 게임 루프가 진행되지 않습니다.

**비동기(Asynchronous)** 로딩은 요청과 완료 시점을 분리합니다. 호출 직후에는 작업을 나타내는 핸들이 반환되고, 실제 로딩은 여러 프레임에 나뉘어 진행됩니다. 에셋은 완료되기 전까지 사용할 수 없지만, 그 사이에도 프레임은 계속 진행될 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="280" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">동기 로딩 vs 비동기 로딩</text>

  <!-- ===== Synchronous Loading (top half) ===== -->
  <text fill="currentColor" x="30" y="55" font-size="11" font-weight="bold" font-family="sans-serif">동기 로딩</text>

  <!-- Timeline bar -->
  <rect x="30" y="65" width="500" height="24" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- Pre-block frame segment -->
  <rect x="30" y="65" width="60" height="24" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="60" y="81" text-anchor="middle" font-size="9" font-family="sans-serif">현재 프레임</text>

  <!-- Blocking load segment (red-ish highlight via higher opacity) -->
  <rect x="90" y="65" width="280" height="24" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="230" y="81" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">에셋 로드 (블로킹)</text>

  <!-- Post-block frame segment -->
  <rect x="370" y="65" width="160" height="24" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="450" y="81" text-anchor="middle" font-size="9" font-family="sans-serif">다음 프레임</text>

  <!-- Spike indicator -->
  <line x1="90" y1="95" x2="90" y2="115" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="370" y1="95" x2="370" y2="115" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="90" y1="115" x2="370" y2="115" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <text fill="currentColor" x="230" y="135" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">완료될 때까지 프레임 진행 중단</text>

  <!-- ===== Asynchronous Loading (bottom half) ===== -->
  <text fill="currentColor" x="30" y="180" font-size="11" font-weight="bold" font-family="sans-serif">비동기 로딩</text>

  <!-- Frame boxes -->
  <rect x="30" y="190" width="110" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="85" y="207" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">프레임 1</text>

  <rect x="160" y="190" width="110" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="215" y="207" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">프레임 2</text>

  <rect x="290" y="190" width="110" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="345" y="207" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">프레임 3</text>

  <rect x="420" y="190" width="110" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="475" y="207" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">프레임 4</text>

  <!-- Loading progress bar spanning frames 1-4 -->
  <rect x="30" y="255" width="370" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>

  <!-- Loading segments inside the bar -->
  <rect x="30" y="255" width="130" height="18" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="95" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 진행</text>

  <rect x="160" y="255" width="110" height="18" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="215" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 진행</text>

  <rect x="270" y="255" width="130" height="18" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="335" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 진행</text>

  <!-- Completion marker -->
  <text fill="currentColor" x="430" y="268" font-size="9" font-weight="bold" font-family="sans-serif">완료</text>

  <!-- Vertical connectors from frames to loading bar -->
  <line x1="85" y1="240" x2="85" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="215" y1="240" x2="215" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="345" y1="240" x2="345" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="475" y1="240" x2="475" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Labels under each frame -->
  <text fill="currentColor" x="85" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">메인 루프 진행</text>
  <text fill="currentColor" x="215" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">메인 루프 진행</text>
  <text fill="currentColor" x="345" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">메인 루프 진행</text>
  <text fill="currentColor" x="475" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">에셋 사용 가능</text>

  <!-- Arrow from loading bar end to frame 4 -->
  <line x1="400" y1="264" x2="418" y2="264" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="420,264 414,260 414,268" fill="currentColor"/>

  <!-- Summary note -->
  <text fill="currentColor" x="280" y="300" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">요청과 완료가 분리되어 프레임 진행 유지</text>
</svg>
</div>

<br>

동기 로딩의 비용은 호출한 프레임에 집중됩니다. Unity의 Update, 입력 처리, 렌더링 명령 생성은 모두 메인 스레드 흐름 안에서 진행되므로, 이 스레드가 로딩 완료를 기다리는 동안 다음 프레임으로 넘어갈 수 없습니다. 화면은 이전 프레임 상태로 멈춰 보이고, 로드해야 하는 에셋과 의존성이 많을수록 이 멈춤도 길어집니다.

비동기 로딩은 이 비용을 한 프레임에 몰지 않고 나누어 처리합니다. 파일 읽기, 데이터 준비, 일부 역직렬화 작업은 백그라운드에서 진행될 수 있고, 텍스처와 메쉬 업로드는 **Async Upload Pipeline(AUP)**의 시간 예산에 맞춰 여러 프레임에 나뉘어 처리될 수 있습니다. 그래서 큰 에셋을 불러오더라도 동기 로딩처럼 한 프레임이 길게 막히는 상황을 줄일 수 있습니다.

다만 비동기 로딩은 비용을 없애는 기능이 아니라 비용을 분산하는 방식입니다. Unity 오브젝트를 최종적으로 등록하고 참조를 연결하는 단계처럼 메인 스레드에서 처리해야 하는 작업은 여전히 남습니다. 씬 로딩처럼 오브젝트가 장면에 통합되는 경우에는 활성화 시점에 `Awake`나 `OnEnable` 같은 콜백도 이어질 수 있습니다. 따라서 비동기 로딩을 사용하더라도 완료 시점에 작업이 몰리면 짧은 스파이크가 생길 수 있습니다.

### AssetBundle과 Addressables

동기와 비동기가 로딩을 호출하고 기다리는 방식의 차이라면, AssetBundle과 Addressables는 에셋을 어떤 단위로 패키징하고 런타임에서 어떻게 찾아올지를 정하는 시스템입니다. 씬에 직접 배치된 에셋은 보통 씬 로딩과 함께 따라오지만, 런타임 중 필요한 콘텐츠를 선택적으로 내려받거나 교체하려면 별도의 에셋 묶음과 로드 경로가 필요합니다.

**AssetBundle**은 여러 에셋을 번들 파일로 묶는 Unity의 저수준 패키징 방식입니다. 빌드 시점에 어떤 에셋을 어떤 번들에 넣을지 정하고, 런타임에서는 해당 번들을 로컬 저장소에서 읽거나 원격 서버에서 내려받아 사용합니다. 개발자가 로드와 언로드 시점을 세밀하게 제어할 수 있는 대신, 번들 간 의존성, 중복 포함, 캐싱, 버전 관리, 해제 타이밍도 직접 설계해야 합니다.

**Addressables**는 이 과정을 주소 기반으로 감싸는 고수준 에셋 관리 시스템입니다. 에셋에 문자열 주소(Address)나 `AssetReference`를 붙여 두면, 코드는 파일 경로나 번들 이름 대신 주소를 통해 로드를 요청합니다. Addressables는 카탈로그를 보고 실제 위치를 찾고, 필요한 의존성을 함께 로드한 뒤, 완료된 작업을 `AsyncOperationHandle`로 돌려줍니다.

해제도 같은 흐름으로 관리됩니다. Addressables는 로드 요청과 의존성에 대해 참조 카운트를 유지하고, `Release`가 호출되면 해당 카운트를 줄입니다. 더 이상 참조하지 않는 에셋과 번들은 해제 대상이 될 수 있습니다. 다만 참조 카운팅이 그룹 설계까지 대신해 주는 것은 아니므로, 어떤 에셋을 같은 그룹에 묶을지와 언제 로드하고 해제할지는 여전히 프로젝트 구조에 맞게 정해야 합니다.

> Addressables의 그룹 구성과 메모리 관리 전략은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 자세히 다룹니다.

---

## Instantiate의 내부 동작

런타임에서 적, 총알, 이펙트처럼 같은 구조의 오브젝트를 새로 만들 때는 `Instantiate(original)`을 사용합니다. 이 함수는 원본 오브젝트를 기준으로 새로운 GameObject 인스턴스를 만들고, 원본이 가진 컴포넌트와 자식 구조를 새 인스턴스 쪽에 구성합니다.

> 프리팹을 런타임에 복제하는 과정은 [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)에서 간략히 다룹니다.

중요한 점은 `Instantiate`가 원본을 통째로 새 파일처럼 복사하는 함수가 아니라는 점입니다. GameObject와 Component 인스턴스는 새로 만들지만, 머티리얼, 텍스처, 메쉬 같은 에셋 참조는 그대로 공유될 수 있습니다. 이 절에서는 `Instantiate`가 무엇을 새로 만들고, 무엇을 공유하며, 그 과정에서 어떤 비용이 발생하는지를 살펴보겠습니다.

### Deep Copy와 Transfer 메커니즘

`Instantiate`는 원본의 주소만 하나 더 들고 있는 **얕은 복사(Shallow Copy)**가 아닙니다. 원본 GameObject를 기준으로 자식 GameObject와 Component를 따라 내려가며, 같은 구조를 가진 새 인스턴스 계층을 만듭니다. 이처럼 오브젝트 그래프 자체를 새로 구성하는 복사를 **깊은 복사(Deep Copy)**라고 볼 수 있습니다.

이 복제가 가능한 이유는 Unity의 직렬화 시스템이 오브젝트마다 어떤 필드를 읽고 써야 하는지 알고 있기 때문입니다. 씬을 저장할 때는 이 규칙을 사용해 필드 값을 파일에 기록하고, `Instantiate`에서는 같은 규칙을 사용해 원본의 직렬화된 필드 값을 새 인스턴스에 복사합니다.

Unity 내부에서 이런 필드 순회와 값 전달에 쓰이는 공통 흐름을 **Transfer**라고 부릅니다. 저장에서는 메모리의 값을 디스크로 옮기고, 로딩에서는 디스크의 값을 메모리로 복원하며, `Instantiate`에서는 원본 오브젝트의 값을 새 오브젝트로 옮기는 식입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="360" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Instantiate 내부 동작</text>

  <!-- ==================== 원본 프리팹 (Left) ==================== -->
  <text fill="currentColor" x="148" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">원본 프리팹</text>
  <rect x="10" y="54" width="275" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <text fill="currentColor" x="24" y="76" font-size="11" font-weight="bold" font-family="sans-serif">Root GameObject</text>
  <line x1="22" y1="82" x2="273" y2="82" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="38" y="100" font-size="10" font-family="sans-serif" opacity="0.7">├─ Transform</text>
  <text fill="currentColor" x="38" y="118" font-size="10" font-family="sans-serif" opacity="0.7">├─ MeshRenderer</text>
  <text fill="currentColor" x="38" y="136" font-size="10" font-family="sans-serif" opacity="0.7">├─ Collider</text>
  <text fill="currentColor" x="38" y="154" font-size="10" font-family="sans-serif" opacity="0.7">└─ EnemyScript</text>
  <text fill="currentColor" x="68" y="170" font-size="9" font-family="sans-serif" opacity="0.5">└─ hp = 100</text>

  <line x1="22" y1="180" x2="273" y2="180" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text fill="currentColor" x="38" y="198" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.8">Child: WeaponHolder</text>
  <text fill="currentColor" x="54" y="216" font-size="10" font-family="sans-serif" opacity="0.7">├─ Transform</text>
  <text fill="currentColor" x="54" y="234" font-size="10" font-family="sans-serif" opacity="0.7">└─ WeaponScript</text>

  <!-- ==================== Instantiate 화살표 (Center) ==================== -->
  <line x1="295" y1="160" x2="424" y2="160" stroke="currentColor" stroke-width="2"/>
  <polygon points="428,160 420,155 420,165" fill="currentColor"/>
  <text fill="currentColor" x="360" y="148" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">Instantiate</text>
  <text fill="currentColor" x="360" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">Deep Copy + Transfer</text>

  <!-- ==================== 복제본 (Right) ==================== -->
  <text fill="currentColor" x="572" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">복제본 (Clone)</text>
  <rect x="435" y="54" width="275" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>

  <text fill="currentColor" x="449" y="76" font-size="11" font-weight="bold" font-family="sans-serif">Root GameObject (Clone)</text>
  <line x1="447" y1="82" x2="698" y2="82" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="463" y="100" font-size="10" font-family="sans-serif" opacity="0.7">├─ Transform</text>
  <text fill="currentColor" x="630" y="100" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>
  <text fill="currentColor" x="463" y="118" font-size="10" font-family="sans-serif" opacity="0.7">├─ MeshRenderer</text>
  <text fill="currentColor" x="630" y="118" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>
  <text fill="currentColor" x="463" y="136" font-size="10" font-family="sans-serif" opacity="0.7">├─ Collider</text>
  <text fill="currentColor" x="630" y="136" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>
  <text fill="currentColor" x="463" y="154" font-size="10" font-family="sans-serif" opacity="0.7">└─ EnemyScript</text>
  <text fill="currentColor" x="630" y="154" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>
  <text fill="currentColor" x="493" y="170" font-size="9" font-family="sans-serif" opacity="0.5">└─ hp = 100 (값 복사)</text>

  <line x1="447" y1="180" x2="698" y2="180" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text fill="currentColor" x="463" y="198" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.8">Child: WeaponHolder (Clone)</text>
  <text fill="currentColor" x="479" y="216" font-size="10" font-family="sans-serif" opacity="0.7">├─ Transform</text>
  <text fill="currentColor" x="630" y="216" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>
  <text fill="currentColor" x="479" y="234" font-size="10" font-family="sans-serif" opacity="0.7">└─ WeaponScript</text>
  <text fill="currentColor" x="630" y="234" font-size="8" font-family="sans-serif" opacity="0.35">새 인스턴스</text>

  <!-- ==================== 공유 에셋 (Bottom Center) ==================== -->
  <text fill="currentColor" x="360" y="320" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">공유 에셋</text>
  <text fill="currentColor" x="360" y="336" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">새로 복제하지 않고 원본과 복제본이 같은 에셋을 참조</text>
  <rect x="140" y="344" width="440" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="185" y="374" font-size="10" font-family="sans-serif" opacity="0.7">Material</text>
  <text fill="currentColor" x="265" y="374" font-size="10" font-family="sans-serif" opacity="0.7">Texture</text>
  <text fill="currentColor" x="345" y="374" font-size="10" font-family="sans-serif" opacity="0.7">Mesh</text>
  <text fill="currentColor" x="405" y="374" font-size="10" font-family="sans-serif" opacity="0.7">Shader</text>
  <text fill="currentColor" x="475" y="374" font-size="10" font-family="sans-serif" opacity="0.7">AudioClip</text>
  <text fill="currentColor" x="548" y="374" font-size="10" font-family="sans-serif" opacity="0.5">...</text>

  <!-- ==================== 참조 화살표: 원본 → 공유 에셋 ==================== -->
  <line x1="148" y1="274" x2="280" y2="344" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="4,3"/>
  <polygon points="282,345 274,337 280,347" fill="currentColor" fill-opacity="0.4"/>
  <text fill="currentColor" x="196" y="298" font-size="8" font-family="sans-serif" opacity="0.4">참조</text>

  <!-- ==================== 참조 화살표: 복제본 → 공유 에셋 ==================== -->
  <line x1="572" y1="274" x2="440" y2="344" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="4,3"/>
  <polygon points="438,345 440,347 446,337" fill="currentColor" fill-opacity="0.4"/>
  <text fill="currentColor" x="518" y="298" font-size="8" font-family="sans-serif" opacity="0.4">같은 참조</text>

  <!-- ==================== 범례 (하단) ==================== -->
  <rect x="20" y="416" width="680" height="36" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="36" y1="434" x2="56" y2="434" stroke="currentColor" stroke-width="2"/>
  <polygon points="60,434 54,431 54,437" fill="currentColor"/>
  <text fill="currentColor" x="68" y="438" font-size="10" font-family="sans-serif">새로 생성: GameObject, Component, 필드 값</text>
  <line x1="400" y1="434" x2="420" y2="434" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <polygon points="424,434 418,431 418,437" fill="currentColor"/>
  <text fill="currentColor" x="432" y="438" font-size="10" font-family="sans-serif">참조 유지: Mesh, Texture, Material, Shader 등</text>
</svg>
</div>

<br>

복제 대상은 GameObject, Component, 그리고 그 안의 직렬화된 필드 값입니다. 원본 계층 안의 오브젝트를 가리키던 참조는 복제본 계층 안의 대응 오브젝트를 가리키도록 다시 연결됩니다. 예를 들어 원본 스크립트가 원본 자식의 Transform을 참조하고 있었다면, 복제본 스크립트는 복제본 자식의 Transform을 참조해야 합니다.

반면 계층 밖에 있는 **공유 에셋(Shared Asset)**은 새로 복제하지 않습니다. Mesh, Texture, Shader, AudioClip 같은 에셋은 원본과 복제본이 같은 인스턴스를 참조합니다. 그래서 적 캐릭터 프리팹을 100번 `Instantiate`해도, 그 프리팹이 사용하는 메쉬나 텍스처 본체가 100개로 늘어나는 것은 아닙니다.

Material은 접근 방식에 따라 주의가 필요합니다. `Instantiate`를 호출하는 순간에는 다른 공유 에셋처럼 참조만 유지됩니다. 하지만 런타임에 `renderer.material`에 접근하면 Unity는 해당 Renderer 전용 Material 인스턴스를 만들 수 있습니다. 여러 오브젝트가 각각 `.material`에 접근하면 Material 사본도 그만큼 늘어날 수 있습니다. 공유 상태를 유지해야 한다면 `.sharedMaterial`을 사용하고, 오브젝트별 색상이나 일부 셰이더 값만 바꾸려면 `MaterialPropertyBlock`을 검토하는 편이 좋습니다.

### Instantiate의 비용

`Instantiate` 비용은 크게 세 곳에서 발생합니다. 첫째는 Deep Copy 자체의 비용입니다. 원본 계층을 따라가며 GameObject와 Component를 새로 만들고, 직렬화된 필드 값을 복사해야 하므로 복제 대상이 클수록 시간이 늘어납니다. 컴포넌트가 많거나 자식 계층이 깊거나, 필드에 큰 배열과 긴 문자열 같은 데이터가 들어 있으면 그만큼 순회하고 복사할 양도 많아집니다.

둘째는 생명주기 콜백 비용입니다. 활성 상태의 오브젝트를 생성하면 새 컴포넌트의 `Awake`와 `OnEnable`이 이어서 호출될 수 있습니다. 이 안에서 다른 오브젝트를 찾거나, 컬렉션을 만들거나, 추가 로드를 요청한다면 그 작업까지 생성 시점의 비용으로 나타납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 제목 -->
  <text x="220" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Instantiate 비용에 영향을 주는 요소</text>
  <!-- 비용 증가 요인 영역 -->
  <rect x="10" y="36" width="420" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">복제 비용을 키우는 요소</text>
  <text x="36" y="82" font-family="sans-serif" font-size="11" fill="currentColor">컴포넌트 수</text>
  <text x="150" y="82" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">새 인스턴스 수 증가</text>
  <text x="36" y="102" font-family="sans-serif" font-size="11" fill="currentColor">자식 오브젝트 수</text>
  <text x="150" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">계층이 깊고 넓을수록 비용 증가</text>
  <text x="36" y="122" font-family="sans-serif" font-size="11" fill="currentColor">직렬화 필드 크기</text>
  <text x="150" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">큰 배열, 긴 문자열, 참조 목록</text>
  <text x="36" y="142" font-family="sans-serif" font-size="11" fill="currentColor">Awake/OnEnable 콜백</text>
  <text x="175" y="142" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">복제 후 호출되는 초기화 코드</text>
  <!-- 구분선 -->
  <line x1="10" y1="186" x2="430" y2="186" stroke="currentColor" stroke-width="1.5"/>
  <!-- 비용에 영향 없는 요소 영역 -->
  <rect x="10" y="186" width="420" height="130" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="210" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">직접 복제하지 않는 요소</text>
  <text x="36" y="234" font-family="sans-serif" font-size="11" fill="currentColor">참조 에셋의 크기</text>
  <text x="160" y="234" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">본체 대신 참조를 복사</text>
  <text x="36" y="254" font-family="sans-serif" font-size="11" fill="currentColor">메쉬 정점 수</text>
  <text x="160" y="254" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메쉬 자체는 복사하지 않음</text>
</svg>
</div>

<br>

정리하면 `Instantiate`의 직접 복제 비용을 키우는 요소는 새로 만들어야 할 GameObject와 Component의 수, 자식 계층의 규모, 직렬화된 필드 데이터의 양입니다. 반대로 참조 중인 텍스처의 해상도나 메쉬의 정점 수는 복제 비용과 직접 연결되지 않습니다. `Instantiate`는 그 본체를 새로 복사하지 않고, 이미 로드된 에셋에 대한 참조를 새 인스턴스에 연결합니다.

셋째는 메모리 할당 비용입니다. 새 오브젝트를 만들면 C# 쪽 래퍼 객체와 엔진 내부 데이터가 함께 준비됩니다. C# 객체는 GC가 관리하는 **관리 힙(Managed Heap)**에 놓이고, Transform, Renderer, Collider처럼 엔진이 직접 다루는 데이터는 **네이티브 메모리(Native Memory)** 쪽에 배치됩니다.

생성한 오브젝트를 `Destroy`해도 두 영역이 같은 방식으로 정리되지는 않습니다. 엔진 쪽 네이티브 데이터는 Unity의 파괴 처리 흐름에 따라 정리되지만, 관리 힙에 남은 C# 래퍼 객체는 곧바로 사라지는 것이 아니라 가비지 컬렉터(GC)의 수거 대상이 됩니다. 생성과 파괴를 짧은 주기로 반복하면 수거해야 할 객체가 계속 쌓이고, GC가 개입할 가능성도 커집니다.

GC가 실행되면 관리 힙을 검사하는 동안 프레임 시간에 영향을 줄 수 있습니다. Unity의 Incremental GC는 수거 작업을 여러 프레임에 나누어 한 번의 큰 스파이크를 줄이는 데 도움을 주지만, 할당 자체가 많으면 결국 처리해야 할 총량은 늘어납니다. 따라서 생성과 파괴가 자주 일어나는 오브젝트라면 GC 설정에 기대기보다 할당량을 줄이는 구조를 먼저 잡아야 합니다.

> 관리 힙에 메모리가 할당되는 구체적인 과정은 [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 자세히 다룹니다.

이때 가장 흔히 쓰는 방법이 **오브젝트 풀링(Object Pooling)**입니다. 필요한 수의 오브젝트를 미리 만들어 비활성 상태로 보관해 두고, 필요할 때 꺼내 활성화한 뒤 사용이 끝나면 다시 비활성화해 풀에 돌려놓습니다. 이렇게 하면 플레이 중 반복되는 `Instantiate`와 `Destroy` 호출이 줄어들어 복제 연산, 메모리 할당, GC 부담을 함께 낮출 수 있습니다.

다만 풀링은 비용을 없애는 것이 아니라 미리 지불하고 재사용하는 방식입니다. 풀에 들어 있는 오브젝트는 비활성 상태에서도 메모리를 차지합니다. 풀을 너무 크게 잡으면 상주 메모리가 늘어나고, 너무 작게 잡으면 부족한 순간에 다시 `Instantiate`가 발생합니다. 따라서 실제 플레이에서 동시에 필요한 개수를 프로파일링하고, 피크 사용량에 맞춰 풀 크기를 정하는 편이 좋습니다.

---

## 참조와 의존성

메모리에 올라오는 에셋의 범위는 로드 요청을 보낸 에셋 하나로 끝나지 않는 경우가 많습니다. 프리팹이 머티리얼을 참조하고, 머티리얼이 텍스처와 셰이더를 참조한다면 프리팹을 로드하는 순간 그 참조 대상들도 함께 필요해집니다.

따라서 메모리 사용량을 볼 때는 에셋의 파일 크기만 볼 수 없습니다. **무엇을 로드하느냐는 곧 어떤 의존성까지 함께 끌고 오는가**의 문제입니다. 앞서 본 연쇄 로딩도 이 참조 관계를 따라 발생하므로, 예상보다 많은 에셋이 올라온다면 먼저 에셋 사이의 연결부터 확인해야 합니다.

### 참조가 만드는 의존성 체인

의존성은 참조 방향을 따라 확장됩니다. 어떤 에셋이 다른 에셋을 참조하고 있으면, 그 에셋을 사용하기 위해 참조 대상도 함께 필요해집니다. 그리고 참조 대상이 다시 다른 에셋을 참조한다면, 그 다음 대상까지 이어서 필요해집니다. 이렇게 로드 대상이 참조를 따라 연쇄적으로 넓어지는 구조를 **의존성 체인(Dependency Chain)**이라고 합니다.

예를 들어 적 프리팹이 MeshRenderer를 가지고 있고, 그 Renderer가 머티리얼을 참조한다고 가정해 보겠습니다. 프리팹을 로드하려면 머티리얼도 필요합니다. 그 머티리얼이 다시 텍스처와 셰이더를 참조한다면, 프리팹 하나를 요청했을 뿐이어도 실제 로딩 범위는 머티리얼, 텍스처, 셰이더까지 넓어집니다.

같은 에셋 참조가 여러 곳에서 반복된다고 해서 매번 새 인스턴스가 생기는 것은 아닙니다. 이미 로드된 에셋은 같은 참조를 통해 재사용될 수 있으므로, 여러 프리팹이 같은 셰이더나 텍스처를 가리킨다면 그 에셋은 하나만 메모리에 올라와도 됩니다. 반대로 프리팹마다 서로 다른 텍스처를 참조한다면, 참조 대상이 늘어난 만큼 메모리 사용량도 함께 늘어납니다.

### 의도하지 않은 의존성

의존성 체인이 길어질수록 로드 범위는 눈에 보이는 사용 범위보다 넓어질 수 있습니다. 코드에서는 작은 프리팹 하나, 스프라이트 하나, 데이터 에셋 하나만 요청했다고 생각해도, 그 에셋이 붙잡고 있는 참조 때문에 더 큰 묶음이 함께 필요해지는 경우가 있습니다. 이런 의존성은 에디터에서 잘 드러나지 않아 메모리 프로파일링을 할 때 뒤늦게 발견되기 쉽습니다.

대표적인 예가 **스프라이트 아틀라스(Sprite Atlas)**입니다. 아틀라스는 여러 스프라이트를 한 장 또는 여러 장의 텍스처로 묶어 렌더링 효율을 높입니다. 하지만 특정 화면에서 아틀라스 안의 스프라이트 하나만 사용하더라도, 런타임에서는 그 스프라이트가 속한 아틀라스 텍스처가 함께 필요할 수 있습니다. 작은 아이콘 하나를 참조했는데 예상보다 큰 텍스처가 메모리에 올라오는 식입니다.

거대한 **ScriptableObject**도 같은 문제를 만들 수 있습니다. 예를 들어 모든 레벨의 배경 텍스처, BGM, 적 프리팹을 하나의 설정 에셋에 직접 참조로 모아 두면, 그 설정 에셋을 로드하는 순간 현재 레벨과 무관한 에셋까지 의존성에 포함될 수 있습니다. 데이터 접근은 편해지지만, 런타임에서는 필요한 데이터만 선택적으로 가져오기 어려운 구조가 됩니다.

이런 문제를 줄이려면 큰 참조 묶음을 용도별로 나눠야 합니다. 레벨별 설정은 레벨 단위로 분리하고, UI 아틀라스도 화면이나 기능 단위로 나누면 필요 없는 에셋이 함께 끌려오는 범위를 줄일 수 있습니다. 메모리가 예상보다 많이 잡힌다면 Unity 에디터에서 에셋을 선택한 뒤 **Select Dependencies**로 참조 체인을 확인하고, 실제 실행 중에는 Memory Profiler로 어떤 에셋이 함께 로드되었는지 확인하는 편이 좋습니다.

---

## Resources 폴더의 문제점

의존성 체인이 실제 메모리와 빌드 크기에 어떤 영향을 주는지는 에셋을 어떤 경로로 로드하느냐에 따라 달라집니다. 같은 에셋이라도 씬에 직접 포함되는지, Addressables로 관리되는지, Resources 폴더에서 문자열로 불러오는지에 따라 빌드 포함 방식과 해제 방식이 달라집니다.

그중 가장 단순한 방식이 **Resources** 폴더입니다. 프로젝트 안에 `Resources`라는 이름의 폴더를 만들고 에셋을 넣어 두면, 런타임에서 `Resources.Load("path/to/asset")`처럼 경로 문자열만으로 해당 에셋을 불러올 수 있습니다. 별도의 번들 구성이나 주소 등록 없이 바로 사용할 수 있다는 점은 작고 단순한 프로젝트에서는 편리합니다.

문제는 이 편의가 프로젝트 규모가 커질수록 통제하기 어려운 비용으로 바뀐다는 점입니다. Resources 폴더에 들어간 에셋은 사용 여부와 관계없이 빌드 포함 대상이 되고, 런타임에서는 문자열 경로와 의존성 체인을 따라 로드됩니다. 그래서 Resources는 쓰기 쉽지만, 빌드 크기, 시작 시간, 메모리 관리 측면에서 구조적인 약점을 가집니다.

### 모든 에셋이 빌드에 포함됨

Resources의 첫 번째 문제는 포함 기준이 코드 사용 여부가 아니라 폴더 위치라는 점입니다. Unity는 `Resources` 폴더 안에 있는 에셋을 런타임에서 언제든 `Resources.Load`로 요청할 수 있다고 보고, 실제 호출 여부와 관계없이 빌드에 포함합니다.

그 결과 임시 텍스처, 사용하지 않는 프리팹, 테스트용 데이터가 폴더에 남아 있기만 해도 최종 빌드 크기에 반영됩니다. 일반 참조 기반 에셋처럼 “아무도 참조하지 않으니 빌드에서 빠진다”는 정리를 기대하기 어렵습니다. Resources를 오래 사용한 프로젝트일수록 폴더 안의 에셋이 실제로 필요한지 주기적으로 정리해야 합니다.

### 인덱스 구성 비용

두 번째 문제는 조회 인덱스입니다. `Resources.Load("path")`는 GUID나 직접 참조가 아니라 문자열 경로로 에셋을 찾습니다. 따라서 런타임에는 어떤 문자열 경로가 어떤 에셋을 가리키는지 빠르게 찾을 수 있는 조회 정보가 필요합니다.

Unity는 빌드에 포함된 Resources 에셋 목록을 바탕으로 이 조회 정보를 준비합니다. 이 초기화는 앱 시작 과정에 포함되므로, Resources 안의 에셋 수가 많을수록 첫 씬이 표시되기 전의 준비 시간이 길어질 수 있습니다.

또한 이 조회 정보는 실행 중에도 유지됩니다. Resources 폴더에 사용하지 않는 에셋이 많이 남아 있으면 빌드 크기만 늘어나는 것이 아니라, 경로 조회를 위한 메타데이터도 함께 커집니다. 프로젝트 규모가 작을 때는 눈에 잘 띄지 않지만, 에셋 수가 수천 개 단위로 늘어나면 시작 시간과 상주 메모리 모두에서 부담이 될 수 있습니다.

### 세밀한 로드/언로드 제어 불가

마지막 문제는 로드한 에셋의 수명을 세밀하게 관리하기 어렵다는 점입니다. Resources는 에셋을 문자열 경로로 쉽게 불러올 수 있게 해 주지만, 어떤 코드가 그 에셋을 얼마나 오래 쓰고 있는지까지 추적해 주지는 않습니다. 그래서 메모리를 내릴 때는 개발자가 직접 정리 시점을 판단해야 합니다.

개별 에셋을 내릴 때는 `Resources.UnloadAsset()`을 사용할 수 있습니다. 이 함수는 텍스처, 메쉬, 오디오클립처럼 디스크에서 로드된 에셋 객체를 대상으로 합니다. 반면 씬에 존재하는 GameObject나 Component 인스턴스를 정리하는 용도는 아니며, 이런 오브젝트는 `Destroy()`로 생명주기를 관리해야 합니다.

`UnloadAsset()`의 한계는 참조 관계를 대신 정리해 주지 않는다는 데 있습니다. 어떤 Renderer나 스크립트가 아직 그 에셋을 가리키고 있다면, 메모리를 내린 뒤에도 참조 구조는 남아 있습니다. 이후 다시 사용되는 순간 에셋이 다시 필요해질 수 있으므로, 개별 언로드만으로는 전체 메모리 상태를 안정적으로 관리하기 어렵습니다.

더 넓은 정리에는 `Resources.UnloadUnusedAssets()`를 사용할 수 있습니다. 이 함수는 더 이상 참조되지 않는 에셋을 찾아 한꺼번에 내립니다. 하지만 사용 여부를 판단하려면 로드된 오브젝트와 참조 관계를 확인해야 하므로 비용이 큽니다. 게임 플레이 중에 호출하면 프레임 스파이크가 생길 수 있어, 보통 로딩 화면이나 씬 전환처럼 멈춤을 감출 수 있는 구간에서 호출합니다.

결국 `UnloadAsset()`은 개별 에셋을 직접 내릴 수 있지만 참조 수명을 관리해 주지는 않고, `UnloadUnusedAssets()`는 넓게 정리할 수 있지만 비용이 큽니다. Resources만으로는 “이 화면에서 필요한 에셋만 올리고, 화면을 벗어나면 정확히 그 묶음만 내리는” 식의 메모리 관리 구조를 만들기 어렵습니다.

<br>

**Resources vs Addressables 비교**

|  | Resources | Addressables |
|---|---|---|
| 빌드 포함 범위 | 폴더 전체 (사용 여부 무관) | 그룹에 등록한 에셋과 의존성 |
| 로드 방식 | 문자열 경로 | 주소(Address) 또는 AssetReference |
| 언로드 | 개별 언로드 또는 전체 unused 정리 | 참조 카운팅 기반 Release |
| 원격 에셋 | 기본 구조에 없음 | 가능 |
| 의존성 관리 | 직접 추적 필요 | 시스템이 의존성 추적 |

<br>

표에서 보듯 Resources는 빠르게 쓰기 쉽지만, 빌드 포함 범위와 메모리 수명 관리를 개발자가 직접 통제하기 어렵습니다. 프로토타입이나 아주 작은 프로젝트에서는 충분할 수 있지만, 런타임 콘텐츠가 많고 메모리 예산이 빡빡한 프로젝트에서는 주된 로딩 구조로 삼기 어렵습니다.

빌드에 포함할 에셋 묶음을 명시적으로 나누고, 로드와 해제를 요청 단위로 추적하려면 Addressables가 더 적합합니다. 특히 모바일처럼 시작 시간과 상주 메모리를 엄격하게 봐야 하는 프로젝트라면, Resources는 제한적인 용도로만 두고 Addressables를 기준으로 에셋 로딩 구조를 설계하는 편이 좋습니다.

> Resources 폴더의 메모리 문제와 Addressables 전환 전략은 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)과 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 각각 다룹니다.

---

## 마무리

이번 글에서는 임포트된 에셋이 디스크에 직렬화되어 저장되고, 런타임에 로드되며, `Instantiate`로 복제되는 흐름을 살펴보았습니다. 핵심은 다음과 같습니다.

- **Unity 직렬화**는 접근 제한자와 어트리뷰트로 저장할 필드를 정하고, 인스턴스에 속하지 않는 `static`·`const`, 다시 대입할 수 없는 `readonly`, 지원하지 않는 타입은 처음부터 제외합니다. `public` 필드는 자동으로 직렬화되고, `private` 필드는 `[SerializeField]`를 붙여야 저장됩니다.
- **[SerializeReference]**는 객체의 실제 타입까지 함께 기록해, 기본 직렬화가 보존하지 못하는 다형성을 지원합니다. 필드에 담기는 객체는 `UnityEngine.Object`를 상속하지 않는 순수 C# 클래스의 인스턴스여야 합니다.
- **ScriptableObject**는 여러 오브젝트가 함께 쓰는 값을 `.asset` 에셋 하나로 분리합니다. 각 오브젝트의 필드에는 값 대신 참조만 저장되므로, 데이터는 메모리에 한 번만 올라옵니다.
- **YAML 씬 파일**은 같은 파일 안의 참조를 fileID로, 다른 에셋을 향한 참조를 GUID와 fileID 조합으로 저장합니다. GUID는 `.meta` 파일에 보관되므로 `.meta` 파일도 소스와 함께 버전 관리에 포함해야 합니다.
- **에셋 로딩**은 참조를 따라 연쇄적으로 일어납니다. 의존성 체인이 길수록 로딩 시간과 메모리 사용량이 함께 늘어나기 쉽습니다.
- **Instantiate**는 GameObject와 Component를 Deep Copy하지만, Mesh나 Texture 같은 공유 에셋은 복제하지 않고 참조만 복사합니다.
- **Resources 폴더**는 안의 모든 에셋이 빌드에 포함되고 세밀한 언로드가 어렵습니다. 시작 시간과 상주 메모리가 중요한 모바일 프로젝트라면 Addressables를 기준으로 에셋 로딩 구조를 설계하는 편이 좋습니다.

정리하면, 이 글의 중심은 무엇이 복사되고 무엇이 공유되는지의 구분입니다. 직렬화 규칙은 인스턴스마다 저장할 값을 정하고, ScriptableObject와 공유 에셋은 복사 대신 참조로 연결됩니다. 이 구분을 알면 Instantiate에 드는 메모리 비용을 예측할 수 있고, 의존성 체인을 따라 불필요한 에셋이 함께 로드되는 문제도 찾을 수 있습니다.

<br>

지금까지 다룬 직렬화, 로딩, Instantiate는 에셋 단위의 동작이고, 의존성 체인은 에셋 사이의 연결입니다. 씬을 로드할 때는 배치된 오브젝트의 역직렬화, 참조 에셋의 연쇄 로딩, 컴포넌트 초기화가 한꺼번에 일어나므로, 씬 전환은 게임 전체에서 메모리 변동과 로딩 스파이크가 크게 나타나기 쉬운 지점입니다.

[Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)에서는 동기/비동기 씬 로딩과 Additive 씬, 그리고 씬을 전환할 때 이전 씬의 메모리를 해제하는 패턴을 다룹니다.

에셋이 차지하는 네이티브 메모리의 사용 패턴은 [메모리 관리 (2)](/dev/unity/MemoryManagement-2/)에서, 런타임에 에셋을 동적으로 올리고 내리는 전략은 [메모리 관리 (3)](/dev/unity/MemoryManagement-3/)에서 이어집니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
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
- **Unity 에셋 시스템 (2) - Serialization과 Instantiation** (현재 글)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
