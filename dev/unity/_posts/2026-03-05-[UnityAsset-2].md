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

[Part 1](/dev/unity/UnityAsset-1/)에서 소스 에셋이 Import Pipeline을 거쳐 엔진 내부 포맷으로 변환되는 과정을 다루었습니다. PNG는 ASTC 텍스처로, FBX는 Unity 메쉬로 변환되어 Library 폴더에 캐싱되며, `.meta` 파일의 GUID가 에셋 간 참조를 유지합니다. Import Settings가 빌드 크기와 메모리에 직접 영향을 주고, AssetPostprocessor로 팀 단위 설정 일관성을 확보할 수 있다는 점도 다루었습니다.

<br>

이 글에서는 변환된 에셋이 디스크에 어떤 형태로 저장되는지(직렬화), 런타임에 메모리로 올라가는 과정(로딩), Instantiate로 복제할 때 내부에서 일어나는 동작을 다룹니다.

직렬화 규칙을 이해하면 Inspector에 필드가 표시되지 않는 이유, 씬 저장 시 데이터가 유실되는 원인을 진단할 수 있습니다. 로딩 과정과 에셋 간 의존성 구조를 파악하면 메모리 사용 패턴이나 로딩 시간 문제의 원인도 추적할 수 있게 됩니다.

---

## 직렬화(Serialization) 개요

**직렬화(Serialization)**는 메모리에 있는 오브젝트의 상태를 바이트 스트림(순서가 정해진 바이트 열)으로 변환하는 과정입니다. 변환된 바이트 스트림은 파일에 저장하거나, 네트워크로 전송하거나, 메모리 안에서 다른 오브젝트로 복원하는 데 사용할 수 있습니다. 반대 방향, 즉 바이트 스트림에서 오브젝트를 복원하는 과정은 **역직렬화(Deserialization)**라 합니다.

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

Unity는 씬, 프리팹, ScriptableObject, 에셋, 프로젝트 설정 등 거의 모든 데이터를 직렬화하여 디스크에 저장합니다. 에디터에서 씬을 저장(Ctrl+S)하면 씬에 있는 모든 GameObject와 컴포넌트가 직렬화되어 `.unity` 파일에 기록됩니다. Play 버튼을 누르면 이 파일을 역직렬화하여 메모리에 오브젝트를 복원합니다.

<br>

직렬화의 첫 번째 용도는 **영속성(Persistence)**입니다. 에디터를 닫았다 다시 열어도 씬 구조, 컴포넌트 값, 에셋 참조가 그대로 남아 있는 것은 직렬화된 데이터가 디스크에 보존되기 때문입니다.

<br>

두 번째 용도는 **복제(Cloning)**입니다. Instantiate 함수는 오브젝트를 복제할 때 내부적으로 직렬화 시스템을 활용합니다. 원본 오브젝트의 필드를 순회하며 값을 읽은 뒤, 그 데이터를 새 오브젝트에 써넣는 방식입니다. 디스크에 기록하지 않고, 메모리 안에서 직렬화와 역직렬화를 수행하여 복제를 완료합니다.

---

## Unity의 직렬화 규칙

Unity의 직렬화 시스템은 C#의 .NET 기본 직렬화(`BinaryFormatter` 등)와 다른 자체 규칙을 따릅니다. Unity는 필드의 접근 제한자(`public`/`private`)와 전용 어트리뷰트(`[SerializeField]`, `[NonSerialized]` 등)로 직렬화 여부를 결정합니다. 이 규칙에 따라 에디터에서 데이터가 저장되는 방식과 Inspector에 표시되는 필드가 달라집니다.

### 자동 직렬화되는 필드

`public` 필드는 별도의 어트리뷰트 없이 자동으로 직렬화됩니다. 어트리뷰트란 대괄호 `[]` 안에 붙여서 필드나 클래스의 동작 방식을 지정하는 표식입니다.

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

`[SerializeField]`를 붙이면 `private` 필드도 직렬화됩니다. 필드가 `private`이므로 외부 코드에서 직접 접근할 수 없고, Inspector에서는 값을 편집할 수 있습니다. 캡슐화(외부에서 내부 데이터를 직접 수정하지 못하도록 접근을 제한하는 설계 원칙)를 유지하면서 Inspector 편집도 가능하므로, `public` 필드보다 `[SerializeField] private` 패턴이 실무에서 권장됩니다.

`static` 필드와 `const` 필드는 인스턴스가 아닌 타입 자체에 속하므로, 인스턴스 단위로 데이터를 저장하는 직렬화 대상에서 제외됩니다. `readonly` 필드는 생성자 이후 값 변경을 금지하므로, 역직렬화 시 값을 써넣을 수 없어 직렬화 대상에서 제외됩니다.

### 직렬화 가능한 타입

접근 제한자와 어트리뷰트로 직렬화 여부를 제어할 수 있지만, 필드의 **타입** 자체가 직렬화를 지원하지 않으면 어떤 설정을 해도 저장되지 않습니다.

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

Dictionary가 직렬화되지 않는 것은 자주 겪는 문제입니다. `public Dictionary<string, int> inventory;`로 선언하면 Inspector에 표시되지 않고, 씬을 저장해도 데이터가 유실됩니다. Dictionary를 저장하려면 `ISerializationCallbackReceiver` 인터페이스를 구현하여 우회합니다. `OnBeforeSerialize()`에서 Dictionary를 키 List와 값 List로 분리하고, `OnAfterDeserialize()`에서 두 List를 다시 Dictionary로 조합합니다.

<br>

### [SerializeReference]로 다형성 지원

타입 제한 외에, 기본 직렬화는 다형성(부모 타입 변수에 자식 객체를 대입하는 것)도 처리하지 못합니다. Unity는 필드의 선언 타입(코드에서 변수를 선언할 때 명시한 타입)으로만 직렬화합니다. 예를 들어 `BaseEffect` 타입으로 선언된 필드에 `FireEffect`(BaseEffect를 상속한 자식 클래스)를 넣어도, `BaseEffect`에 정의된 필드만 저장됩니다. `FireEffect`에 추가한 `damage` 같은 고유 필드는 직렬화 과정에서 무시됩니다.

Unity 2019.3에서 도입된 `[SerializeReference]`는 이 문제를 해결합니다. `[SerializeReference]`를 붙이면 Unity가 실제로 대입된 객체의 런타임 타입을 함께 기록하므로, 인터페이스나 추상 클래스 타입의 필드에서도 자식 클래스의 고유 필드까지 직렬화됩니다.

<br>

```csharp
// [SerializeReference]의 효과

// 기본 직렬화 (값 기반):
  [Serializable] class BaseEffect { int duration; }
  class FireEffect : BaseEffect { int damage; }

  public BaseEffect effect;
  // → Inspector에서 BaseEffect 필드만 표시
  // → FireEffect를 넣어도 damage 필드가 저장되지 않음

// [SerializeReference] 사용:
  [SerializeReference]
  public BaseEffect effect;
  // → Inspector에서 실제 타입(FireEffect)의 모든 필드 표시
  // → 다형성 유지
```

<br>

`[SerializeReference]`에는 몇 가지 제약이 있습니다. 대상 타입은 `UnityEngine.Object`를 상속하지 않는 순수 C# 클래스여야 합니다. MonoBehaviour나 ScriptableObject처럼 `UnityEngine.Object`를 상속하는 타입은 엔진이 별도의 직렬화 경로(에셋 참조, 인스턴스 ID 기반 수명 관리)로 처리하므로, managed reference 방식과 호환되지 않습니다. C# 값 타입(struct)도 지원하지 않으며, 반드시 참조 타입(class)이어야 합니다.

타입 정보는 클래스 이름(네임스페이스 포함)과 어셈블리 이름 문자열로 저장됩니다. 클래스 이름이나 네임스페이스를 변경하면 기존에 직렬화된 데이터를 역직렬화할 수 없게 됩니다. Unity 2021 LTS부터는 `MovedFrom` 어트리뷰트로 타입 이름 변경 시 마이그레이션을 지원하지만, 프리팹 오버라이드 등 일부 상황에서는 동작하지 않는 알려진 제한이 있습니다.

이러한 제약이 있는 대신, 기본 직렬화에 없는 기능도 제공합니다. 기본 직렬화에서는 null 필드가 빈 인스턴스로 대체되고, 같은 객체를 가리키는 두 필드가 별도 복사본으로 직렬화됩니다. `[SerializeReference]`는 null 값을 그대로 보존하고, 공유 참조(여러 필드가 같은 객체를 가리키는 구조)도 유지합니다.

### ScriptableObject — 데이터 공유와 중복 제거

MonoBehaviour에 게임 데이터를 직접 넣으면 인스턴스마다 동일한 값이 복제됩니다. **ScriptableObject**는 이 중복을 제거하는 데이터 컨테이너입니다. 씬의 GameObject에 부착되는 MonoBehaviour와 달리 씬에 종속되지 않으며, `.asset` 파일로 디스크에 직렬화되어 저장됩니다. 여러 오브젝트가 같은 ScriptableObject를 참조하여 데이터를 공유할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="280" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">ScriptableObject를 사용한 데이터 공유</text>

  <!-- === Top section: MonoBehaviour에 직접 데이터를 넣는 경우 === -->
  <text fill="currentColor" x="280" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">MonoBehaviour에 직접 데이터를 넣는 경우</text>

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
  <text fill="currentColor" x="280" y="198" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">→ 같은 데이터가 인스턴스마다 복제됨 (메모리 낭비)</text>

  <!-- === Divider === -->
  <line x1="40" y1="220" x2="520" y2="220" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- === Bottom section: ScriptableObject로 공유하는 경우 === -->
  <text fill="currentColor" x="280" y="250" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">ScriptableObject로 공유하는 경우</text>

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
  <text fill="currentColor" x="280" y="514" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">→ 데이터가 한 곳에만 존재 (참조로 공유)</text>
</svg>
</div>

<br>

ScriptableObject는 에셋이므로, 100개의 적 인스턴스가 같은 ScriptableObject를 참조해도 메모리에 한 번만 로드됩니다. 게임 디자인 데이터(스탯, 아이템 정보, 스킬 정보 등)를 ScriptableObject로 관리하면 메모리 중복을 제거할 수 있고, 데이터를 수정할 때도 한 곳만 바꾸면 모든 참조에 즉시 반영됩니다.

단, 런타임에 ScriptableObject의 값을 변경하면 해당 세션에서는 모든 참조에 반영되지만, 빌드 환경에서는 앱을 재시작하면 원래 값으로 돌아갑니다. 반면 에디터에서는 ScriptableObject가 에셋 파일 자체를 메모리에 올린 것이므로, 플레이 모드 중 변경한 값이 에셋의 메모리 상태에 직접 반영됩니다. 플레이 모드를 종료해도 이 변경은 복원되지 않고, Unity가 에셋을 저장하는 시점(씬 저장, 에디터 종료 등)에 `.asset` 파일에 기록되어 의도하지 않은 데이터 변경이 발생할 수 있습니다.

---

## YAML 씬 파일 구조

Unity의 씬 파일(`.unity`)과 프리팹 파일(`.prefab`)은 텍스트 기반의 **YAML** 형식으로 저장됩니다. YAML은 들여쓰기로 계층 구조를 표현하는 데이터 직렬화 포맷으로, 텍스트 에디터에서 직접 내용을 확인하고 편집할 수 있습니다.

이 YAML 형식은 프로젝트 설정(Edit → Project Settings → Editor)의 직렬화 모드가 **Force Text**(기본값)일 때 적용됩니다. Binary 모드로 전환하면 사람이 읽을 수 없는 바이너리로 저장되므로, 버전 관리와 디버깅을 위해 Force Text를 유지하는 것이 일반적입니다.

YAML 씬 파일의 내부 구조를 이해하면 씬에서 참조가 깨지는 원인을 진단하거나, 버전 관리에서 씬 병합 충돌을 해결할 때 파일을 직접 읽고 수정할 수 있습니다.

### fileID와 오브젝트 식별

씬 파일 내부에서 각 오브젝트(GameObject, Component 등)는 **fileID**라는 파일 내 고유 번호로 식별됩니다. 각 오브젝트 블록은 `--- !u!<classID> &<fileID>` 형식의 헤더로 시작합니다. `!u!` 뒤의 숫자는 **classID** — Unity가 내부 타입마다 부여한 고정 번호입니다(예: 1=GameObject, 4=Transform, 23=MeshRenderer). `&` 뒤의 숫자가 이 파일 안에서 해당 오브젝트를 유일하게 식별하는 fileID입니다.

<br>

```yaml
# .unity 파일의 YAML 구조 (간략화)

--- !u!1 &100000                      # GameObject, fileID = 100000
GameObject:
  m_Name: Player
  m_Component:
    - component: {fileID: 100001}     # Transform 참조
    - component: {fileID: 100002}     # MeshRenderer 참조

--- !u!4 &100001                      # Transform, fileID = 100001
Transform:
  m_LocalPosition: {x: 0, y: 1, z: 0}
  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}
  m_GameObject: {fileID: 100000}      # 소속 GameObject 역참조

--- !u!23 &100002                     # MeshRenderer, fileID = 100002
MeshRenderer:
  m_Materials:
    - {fileID: 2100000, guid: abc123..., type: 2}
    #    ↑                  ↑                  ↑
    # 에셋 내부의        에셋의 GUID        type 2 = 프로젝트 내
    # 서브 오브젝트 번호  (.meta 파일에 기록)  외부 에셋
```

<br>

같은 파일 내의 오브젝트를 참조할 때는 fileID만 사용합니다. 위 예시에서 GameObject가 자신의 Transform과 MeshRenderer를 참조하는 부분이 이에 해당합니다.

다른 파일의 에셋(텍스처, 머티리얼, 프리팹 등)을 참조할 때는 **GUID + fileID** 조합을 사용합니다. GUID는 대상 에셋의 `.meta` 파일에 기록된 고유 식별자이고, fileID는 그 에셋 내부의 특정 서브 오브젝트를 가리킵니다. 하나의 에셋 파일 안에 여러 오브젝트가 포함될 수 있기 때문입니다 — 예를 들어 FBX 파일 안에는 메쉬, 애니메이션 클립, 내장 머티리얼이 각각 별도의 서브 오브젝트로 존재합니다.

`type` 필드는 참조 대상의 종류를 구분합니다. `type: 2`는 프로젝트 내 외부 에셋, `type: 3`은 스크립트나 빌트인 리소스를 가리킵니다.

### .meta 파일과 GUID의 관계

[Part 1](/dev/unity/UnityAsset-1/)에서 `.meta` 파일이 에셋의 GUID를 보관한다는 점을 다루었습니다. 위에서 본 YAML 참조 구조가 바로 이 GUID를 사용하는 지점입니다. 씬 파일에 기록된 GUID가 `.meta` 파일을 거쳐 실제 에셋 파일로 연결되는 흐름을 정리하면 다음과 같습니다.

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
  <text fill="currentColor" x="330" y="192" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">파일 이름이나 경로가 변경되어도 GUID가 유지되면 참조 유효</text>
  <text fill="currentColor" x="330" y="210" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">.meta 파일 삭제 = GUID 재생성 = 모든 참조 깨짐</text>
</svg>
</div>

<br>

`.meta` 파일을 버전 관리에 반드시 포함해야 하는 이유가 이 참조 체인에 있습니다. `.meta` 파일이 사라지면 GUID가 재생성되고, 해당 에셋을 참조하던 씬·프리팹의 모든 연결이 끊어집니다.

에셋 파일을 이동하거나 이름을 변경할 때는 반드시 Unity 에디터의 Project 창에서 수행해야 합니다. 에디터 안에서 이동하면 `.meta` 파일이 함께 갱신되어 GUID가 유지됩니다. 반면 OS 탐색기나 터미널에서 직접 옮기면 `.meta` 파일이 원래 위치에 남아 분리되고, Unity가 이동된 파일을 새 에셋으로 인식하여 새 GUID를 부여하므로 기존 참조가 모두 깨집니다.

---

## 에셋 로딩 과정

직렬화되어 디스크에 저장된 데이터는 그 자체로는 게임에 사용할 수 없습니다. **에셋 로딩**은 게임 실행 시 이 데이터를 디스크에서 읽어 메모리에 오브젝트로 복원하는 과정입니다.

### 로딩의 기본 흐름

에셋 로딩은 세 단계로 진행됩니다. 먼저 에셋 파일의 헤더를 읽어 포함된 오브젝트 목록과 의존성 정보를 파악합니다. 그 다음 참조된 에셋이 아직 메모리에 없으면 먼저 로드한 뒤, 바이트 데이터를 오브젝트로 역직렬화합니다. 마지막으로 복원된 데이터를 용도에 맞는 메모리 영역에 배치합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 590" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="210" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">에셋 로딩 과정</text>

  <!-- Step 1: Header reading -->
  <rect x="30" y="40" width="360" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="62" font-size="12" font-weight="bold" font-family="sans-serif">1. 헤더 읽기</text>
  <line x1="40" y1="70" x2="380" y2="70" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="44" y="90" font-size="10" font-family="sans-serif">에셋 파일의 헤더를 읽어</text>
  <text fill="currentColor" x="44" y="106" font-size="10" font-family="sans-serif">포함된 오브젝트 목록과 의존성 파악</text>
  <text fill="currentColor" x="44" y="130" font-size="9" font-family="sans-serif" opacity="0.5">"이 머티리얼은 텍스처 A와 셰이더 B를 참조하고 있다"</text>

  <!-- Arrow 1→2 -->
  <line x1="210" y1="150" x2="210" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,186 205,176 215,176" fill="currentColor"/>

  <!-- Step 2: Dependency resolution & deserialization -->
  <rect x="30" y="190" width="360" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="212" font-size="12" font-weight="bold" font-family="sans-serif">2. 의존성 해결 및 역직렬화</text>
  <line x1="40" y1="220" x2="380" y2="220" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="44" y="240" font-size="10" font-family="sans-serif">참조하는 에셋이 아직 로드되지 않았으면 먼저 로드 (연쇄 로딩)</text>
  <text fill="currentColor" x="44" y="264" font-size="10" font-family="sans-serif">바이트 데이터를 읽어 오브젝트 복원</text>
  <text fill="currentColor" x="44" y="284" font-size="9" font-family="sans-serif" opacity="0.5">타입 정보 → 필드 매핑 → 값 설정</text>

  <!-- Arrow 2→3 -->
  <line x1="210" y1="310" x2="210" y2="340" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,346 205,336 215,336" fill="currentColor"/>

  <!-- Step 3: Memory placement -->
  <rect x="30" y="350" width="360" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="44" y="372" font-size="12" font-weight="bold" font-family="sans-serif">3. 메모리 배치</text>
  <line x1="40" y1="380" x2="380" y2="380" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Memory mapping items -->
  <text fill="currentColor" x="60" y="404" font-size="10" font-family="sans-serif">텍스처</text>
  <line x1="100" y1="400" x2="170" y2="400" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="174,400 168,397 168,403" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="180" y="404" font-size="10" font-family="sans-serif">GPU 전용 메모리 *</text>

  <text fill="currentColor" x="60" y="428" font-size="10" font-family="sans-serif">메쉬 버퍼</text>
  <line x1="118" y1="424" x2="170" y2="424" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>
  <polygon points="174,424 168,421 168,427" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="180" y="428" font-size="10" font-family="sans-serif">GPU 전용 메모리 *</text>

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

세 단계 중 로딩 시간에 가장 큰 영향을 주는 것은 2단계의 **연쇄 로딩**입니다. 에셋 A가 에셋 B를 참조하고, B가 다시 C를 참조하면, A를 로드하기 위해 B와 C도 함께 로드해야 합니다.
의존성 체인이 길고 넓을수록 로딩 시간과 메모리 사용량이 함께 증가합니다. 예를 들어, 하나의 프리팹이 머티리얼을 참조하고, 그 머티리얼이 텍스처 3장과 셰이더를 참조하면, 프리팹 하나를 로드하기 위해 총 5개의 에셋이 추가로 로드됩니다.

### 동기 로딩 vs 비동기 로딩

에셋 로딩은 동기(Synchronous)와 비동기(Asynchronous) 방식으로 나뉩니다. 동기 로딩은 완료될 때까지 프레임이 멈추고, 비동기 로딩은 여러 프레임에 걸쳐 분산됩니다.

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
  <text fill="currentColor" x="60" y="81" text-anchor="middle" font-size="9" font-family="sans-serif">프레임</text>

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
  <text fill="currentColor" x="230" y="135" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">로딩 완료까지 게임 멈춤 (프레임 스파이크)</text>

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
  <text fill="currentColor" x="95" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 (일부)</text>

  <rect x="160" y="255" width="110" height="18" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="215" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 (일부)</text>

  <rect x="270" y="255" width="130" height="18" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="335" y="268" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">로딩 (일부)</text>

  <!-- Completion marker -->
  <text fill="currentColor" x="430" y="268" font-size="9" font-weight="bold" font-family="sans-serif">완료</text>

  <!-- Vertical connectors from frames to loading bar -->
  <line x1="85" y1="240" x2="85" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="215" y1="240" x2="215" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="345" y1="240" x2="345" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="475" y1="240" x2="475" y2="255" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Labels under each frame -->
  <text fill="currentColor" x="85" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">게임 계속 실행됨</text>
  <text fill="currentColor" x="215" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">게임 계속 실행됨</text>
  <text fill="currentColor" x="345" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">게임 계속 실행됨</text>
  <text fill="currentColor" x="475" y="228" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">에셋 사용 가능</text>

  <!-- Arrow from loading bar end to frame 4 -->
  <line x1="400" y1="264" x2="418" y2="264" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="420,264 414,260 414,268" fill="currentColor"/>

  <!-- Summary note -->
  <text fill="currentColor" x="280" y="300" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">로딩 작업이 여러 프레임에 분산되어 게임이 멈추지 않음</text>
</svg>
</div>

<br>

Unity의 게임 루프(Update → 렌더링)는 메인 스레드에서 실행됩니다. 동기 로딩이 메인 스레드를 점유하면 게임 루프가 진행되지 않으므로, 프레임 스파이크의 크기는 에셋 자체의 크기와 의존성 체인에 포함된 에셋 수에 비례합니다.

<br>

비동기 로딩에서는 오브젝트 역직렬화를 워커 스레드에서 처리하고, 텍스처와 메쉬의 GPU 업로드는 Async Upload Pipeline(AUP)이 렌더 스레드에서 프레임당 일정 시간(기본 2ms)만큼 나누어 수행합니다.
다만, Awake 콜백이나 오브젝트 등록처럼 메인 스레드에서 처리해야 하는 통합 단계가 남아 있으므로, 대량의 오브젝트를 한꺼번에 로드하면 통합 시점에 짧은 스파이크가 발생할 수 있습니다.

### AssetBundle과 Addressables

동기와 비동기는 에셋을 "어떤 방식으로" 메모리에 올릴지를 결정합니다.
이와 별도로, "어떤 단위로" 에셋을 묶어서 로드할지를 결정하는 번들링 시스템이 있습니다. 씬에 직접 배치한 에셋은 씬 로딩 시 자동으로 함께 로드되지만, 런타임에 동적으로 에셋을 로드해야 하는 경우에는 번들링 시스템이 필요합니다.

<br>

**AssetBundle**은 여러 에셋을 하나의 파일로 묶어 패키징하는 시스템입니다. 빌드 시 지정한 에셋들이 하나의 번들 파일로 압축되고, 런타임에 이 번들을 로컬 저장소나 원격 서버에서 로드할 수 있습니다. 어떤 번들을 언제 로드하고 언로드할지 개발자가 직접 제어할 수 있지만, 번들 간 의존성 관리와 번들 구성도 직접 설계해야 합니다.

<br>

**Addressables**는 AssetBundle 위에 구축된 고수준 시스템입니다. 각 에셋에 문자열 주소(Address)를 부여하고, 이 주소만으로 로드와 해제를 수행합니다. AssetBundle에서 직접 관리해야 했던 의존성 해결과 번들 로드/언로드가 내부에서 자동 처리됩니다.

<br>

Addressables는 메모리 관리에 참조 카운팅 방식을 사용합니다. 에셋을 로드할 때마다 내부 카운트가 1 증가하고, 해제할 때마다 1 감소합니다. 카운트가 0이 되면 해당 에셋이 메모리에서 제거됩니다. Addressables의 그룹 구성과 메모리 관리 전략은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 다룹니다.

---

## Instantiate의 내부 동작

`Instantiate(original)` 함수는 원본 오브젝트의 복제본을 생성합니다.
[Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)에서 프리팹의 런타임 복제를 간략히 다루었습니다.

여기서는 Instantiate가 내부적으로 직렬화 시스템을 활용하는 과정과, 그에 따른 복제 범위 및 비용을 구체적으로 살펴봅니다.

### Deep Copy와 Transfer 메커니즘

Instantiate는 참조만 복사하는 얕은 복사(Shallow Copy)가 아니라 **Deep Copy**(깊은 복사)를 수행합니다. 원본 GameObject의 모든 컴포넌트, 자식 오브젝트, 자식의 컴포넌트까지 전부 새로운 인스턴스로 복제됩니다.

직렬화 시스템은 각 오브젝트에 대해 어떤 필드를 읽고 써야 하는지 이미 알고 있습니다. 씬을 저장할 때는 이 로직으로 필드 값을 디스크에 기록합니다.
Instantiate도 같은 로직을 활용하되, 필드 값을 디스크가 아닌 새 오브젝트의 대응 필드에 복사합니다. Unity 내부에서는 이 필드 순회-복사 로직을 **Transfer**라고 부릅니다.

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
  <text fill="currentColor" x="360" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">Deep Copy (Transfer)</text>

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
  <text fill="currentColor" x="360" y="336" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">복사하지 않음 — 원본과 복제본이 같은 인스턴스를 참조</text>
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
  <text fill="currentColor" x="68" y="438" font-size="10" font-family="sans-serif">복제 대상: GameObject, Component, 직렬화된 필드 값</text>
  <line x1="400" y1="434" x2="420" y2="434" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <polygon points="424,434 418,431 418,437" fill="currentColor"/>
  <text fill="currentColor" x="432" y="438" font-size="10" font-family="sans-serif">참조 공유: Mesh, Texture, Material, Shader 등</text>
</svg>
</div>

<br>

적 캐릭터 프리팹을 100번 Instantiate해도 **공유 에셋**(Mesh, Texture, Material, Shader, AudioClip 등)은 메모리에 한 벌만 존재합니다. Instantiate가 이 에셋들을 복사하지 않고, 원본을 가리키는 참조만 복제하기 때문입니다.

<br>

단, Material은 예외적인 동작이 있습니다.

Instantiate 시점에는 다른 공유 에셋과 마찬가지로 참조만 복사됩니다.
그러나 런타임에 스크립트에서 `renderer.material` 프로퍼티에 접근하면, Unity가 그 시점에 Material 인스턴스를 자동 복제합니다. 100개의 오브젝트가 각각 `.material`에 접근하면 100개의 Material 사본이 메모리에 생깁니다. 개별 Material 변경이 필요 없다면 `.sharedMaterial`을 사용하여 공유 상태를 유지해야 합니다.

### Instantiate의 비용

Instantiate는 복제 대상의 모든 컴포넌트와 자식 오브젝트를 순회하며 직렬화된 필드를 하나씩 복사하므로, 컴포넌트 수와 자식 오브젝트 수, 직렬화 필드 크기에 비례하여 비용이 증가합니다.
복제 직후 각 컴포넌트의 Awake와 OnEnable 콜백이 호출되므로, 콜백의 처리 시간도 전체 비용에 포함됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 제목 -->
  <text x="220" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Instantiate 비용에 영향을 주는 요소</text>
  <!-- 비용 증가 요인 영역 -->
  <rect x="10" y="36" width="420" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">비용 증가 요인</text>
  <text x="36" y="82" font-family="sans-serif" font-size="11" fill="currentColor">컴포넌트 수</text>
  <text x="150" y="82" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">많을수록 복제해야 할 객체 증가</text>
  <text x="36" y="102" font-family="sans-serif" font-size="11" fill="currentColor">자식 오브젝트 수</text>
  <text x="150" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">계층이 깊고 넓을수록 비용 증가</text>
  <text x="36" y="122" font-family="sans-serif" font-size="11" fill="currentColor">직렬화 필드 크기</text>
  <text x="150" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">큰 배열, 긴 문자열 등</text>
  <text x="36" y="142" font-family="sans-serif" font-size="11" fill="currentColor">Awake/OnEnable 콜백</text>
  <text x="175" y="142" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">복제 후 호출되는 초기화 코드</text>
  <!-- 구분선 -->
  <line x1="10" y1="186" x2="430" y2="186" stroke="currentColor" stroke-width="1.5"/>
  <!-- 비용에 영향 없는 요소 영역 -->
  <rect x="10" y="186" width="420" height="130" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="26" y="210" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">비용에 영향 없는 요소</text>
  <text x="36" y="234" font-family="sans-serif" font-size="11" fill="currentColor">참조 에셋의 크기</text>
  <text x="160" y="234" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">텍스처가 크든 작든 참조만 복사</text>
  <text x="36" y="254" font-family="sans-serif" font-size="11" fill="currentColor">메쉬 정점 수</text>
  <text x="160" y="254" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메쉬 자체는 복사하지 않음</text>
</svg>
</div>

<br>

복제 연산 비용 외에 메모리 할당 비용도 존재합니다.
Instantiate를 호출하면 두 영역에서 메모리가 할당됩니다. C# 관리 힙(GC가 관리하는 C# 객체 영역)에는 컴포넌트 래퍼 객체가, 네이티브 메모리(Unity 엔진이 C++로 관리하는 영역)에는 엔진 내부 데이터가 할당됩니다.

Instantiate로 생성한 오브젝트를 Destroy로 파괴하면, 네이티브 측 데이터는 해당 프레임 말에 해제됩니다.
반면 관리 힙의 C# 래퍼 객체는 즉시 해제되지 않고 GC(가비지 컬렉터) 수거 대상으로 남습니다. 생성-파괴 사이클이 빈번하면 수거 대상이 누적되어 GC 호출 빈도가 높아집니다.

Unity가 기본으로 사용하는 Boehm GC는 수거 시 메인 스레드를 일시 정지(stop-the-world)시키므로, GC가 자주 동작할수록 프레임 스파이크가 발생합니다. Unity 2019.1부터 제공되는 Incremental GC 옵션을 사용하면 수거 작업을 여러 프레임에 분산할 수 있지만, 할당량 자체를 줄이는 것이 근본적인 해결책입니다.
관리 힙 할당의 상세 메커니즘은 [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룹니다.

이 비용을 줄이는 대표적인 방법이 **오브젝트 풀링**(미리 생성해 둔 오브젝트를 비활성 상태로 보관했다가 재사용하는 패턴)입니다. 풀링을 적용하면 Instantiate/Destroy 호출 자체를 최소화하여 복제 연산과 GC 부담을 모두 줄일 수 있습니다. 다만, 풀에 보관된 오브젝트는 비활성 상태에서도 메모리에 상주합니다.
풀 크기가 과도하면 메모리 압박이 되고, 부족하면 런타임에 추가 Instantiate가 발생합니다. 실제 사용 패턴을 프로파일링하여 풀 크기를 조절하는 것이 핵심입니다.

---

## 참조와 의존성

에셋 간 참조는 로딩 시점에 **어떤 에셋이 함께 메모리에 올라오는지**를 결정합니다. 앞서 로딩 과정에서 살펴본 연쇄 로딩이 바로 이 참조를 따라 작동합니다.

### 참조가 만드는 의존성 체인

하나의 에셋이 다른 에셋을 참조하면, Unity는 참조된 에셋도 함께 로드합니다. 참조된 에셋이 또 다른 에셋을 참조하면 그 에셋까지 로드되며, 이 과정이 재귀적으로 반복되어 의존성 체인을 형성합니다.

<br>

프리팹을 로드하면 의존성 체인에 포함된 모든 에셋이 함께 메모리에 올라옵니다. 적 프리팹이 메쉬, 텍스처, 셰이더를 참조한다면 세 에셋이 모두 로드됩니다.
이때 이미 메모리에 있는 에셋은 중복 로드되지 않으므로, 다른 프리팹이 같은 셰이더를 참조해도 셰이더는 메모리에 한 벌만 유지됩니다.
반면, 프리팹마다 고유한 텍스처를 사용하면 텍스처 수만큼 메모리가 늘어납니다.

### 의도하지 않은 의존성

런타임에 실제로 접근하는 에셋은 일부인데, 참조 구조 때문에 관련된 에셋 전체가 메모리에 올라오는 경우가 있습니다.
전형적인 사례가 **스프라이트 아틀라스**와 **거대한 ScriptableObject**입니다.

스프라이트 아틀라스는 여러 개별 스프라이트를 하나의 텍스처로 묶어 놓은 에셋인데, 아틀라스에 속한 스프라이트 하나를 참조하면 그 스프라이트가 포함된 텍스처 전체가 로드됩니다.

거대한 ScriptableObject도 같은 문제를 일으킵니다. 모든 레벨의 배경 텍스처와 BGM을 한 ScriptableObject에 참조로 모아 두면, 이 ScriptableObject를 로드할 때 참조된 모든 레벨의 에셋이 메모리에 올라옵니다.

<br>

이런 의도하지 않은 의존성은 Unity 에디터에서 에셋을 선택한 후 **Select Dependencies** 기능으로 확인할 수 있습니다.
프로파일링에서 예상보다 메모리 사용량이 높다면, 의존성 체인을 통해 불필요한 에셋이 함께 로드되고 있을 가능성이 높습니다.

---

## Resources 폴더의 문제점

의존성 체인의 영향 범위는 에셋을 어떻게 로드하느냐에 따라 달라집니다.

그 중 가장 단순하면서도 문제가 많은 로딩 방법이 **Resources** 폴더입니다.

Resources 폴더는 Unity가 제공하는 가장 기본적인 런타임 에셋 로딩 수단으로, `Resources.Load("path/to/asset")`처럼 문자열 경로만으로 에셋에 접근할 수 있어 편리합니다. 하지만 빌드 크기, 메모리, 로딩 시간 면에서 구조적 문제가 있습니다.

### 모든 에셋이 빌드에 포함됨

Resources 폴더에 있는 **모든 에셋**은 빌드에 포함됩니다. 실제로 `Resources.Load`로 호출하는지 여부와 무관합니다. 
테스트용으로 넣어둔 텍스처, 더 이상 사용하지 않는 프리팹, 실험적 데이터 — 모두 빌드 파일에 들어갑니다.

<br>

### 인덱스 구성 비용

`Resources.Load("path")`는 문자열 경로로 에셋을 찾으므로, 경로와 에셋을 매핑하는 조회 테이블(인덱스)이 필요합니다.
Unity는 앱이 시작될 때 Resources 폴더의 모든 에셋에 대해 이 인덱스를 메모리에 구성하며, 인덱스 구성이 완료되어야 앱의 첫 씬이 로드됩니다.

Resources 폴더에 수천 개 이상의 에셋이 누적되면, 인덱스 구성만으로 모바일 기기에서 앱 시작 시간이 수 초 이상 길어질 수 있습니다.
인덱스 자체도 앱이 실행되는 동안 메모리에 상주하므로, 사용하지 않는 에셋이 Resources 폴더에 남아 있는 것만으로도 상주 메모리가 낭비됩니다.

### 세밀한 로드/언로드 제어 불가

Resources 폴더의 에셋은 세밀하게 언로드하기 어렵습니다.

`Resources.UnloadAsset()`은 특정 에셋의 네이티브 메모리를 해제합니다. 다만 텍스처·메쉬·오디오클립처럼 네이티브 메모리에 데이터가 로드되는 에셋에만 사용할 수 있고, GameObject나 컴포넌트에는 사용할 수 없습니다.
해제한 에셋을 여전히 참조하는 오브젝트가 있으면, 해당 에셋에 접근하는 시점에 디스크에서 다시 로드됩니다. 메모리를 해제하더라도 참조가 살아있으면 곧바로 재로드되므로, 의도한 메모리 절감 효과를 얻기 어렵습니다.

`Resources.UnloadUnusedAssets()`는 참조되지 않는 모든 에셋을 해제합니다. 이 API는 내부적으로 전체 에셋과 참조 관계를 스캔하기 때문에 비용이 높고, 프레임 스파이크를 유발할 수 있습니다.

개별 해제(`UnloadAsset`)는 참조가 남아 있으면 재로드되고, 일괄 해제(`UnloadUnusedAssets`)는 전체 스캔 비용이 높습니다.
결국 Resources 폴더에서는 런타임 메모리를 세밀하게 관리할 수단이 사실상 없습니다.

<br>

**Resources vs Addressables 비교**

|  | Resources | Addressables |
|---|---|---|
| 빌드 포함 범위 | 폴더 전체 (사용 여부 무관) | 명시적으로 지정한 에셋만 |
| 로드 방식 | 문자열 경로 | 주소(Address) 또는 AssetReference |
| 언로드 | 전체 스캔 방식 (UnloadUnusedAssets) | 참조 카운팅 기반 (개별 해제 가능) |
| 원격 에셋 | 불가 | 가능 (CDN에서 다운) |
| 의존성 관리 | 수동 | 자동 |

<br>

Unity 공식 문서에서도 Resources 폴더 사용을 권장하지 않습니다. 프로토타입이나 소규모 프로젝트에서는 편의상 사용할 수 있지만, 모바일 출시를 목표로 하는 프로젝트에서는 Addressables 전환이 권장됩니다.

Resources 폴더의 메모리 문제와 Addressables 전환 전략은 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)과 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 각각 다룹니다.

---

## 마무리

- public 필드는 자동 직렬화되며, private 필드는 `[SerializeField]`로 명시합니다. Dictionary, 인터페이스 등 일부 타입은 기본 직렬화를 지원하지 않습니다.
- ScriptableObject는 데이터를 에셋으로 분리하여 인스턴스 간 메모리 공유를 가능하게 합니다.
- 씬 파일은 YAML 형식으로 저장되며, 내부 참조는 fileID로, 외부 참조는 GUID + fileID 조합으로 식별됩니다.
- 에셋 로딩 시 참조 에셋이 연쇄적으로 함께 로드되므로, 의존성 체인에 포함된 에셋이 많을수록 메모리와 로딩 시간이 증가합니다.
- Instantiate는 GameObject와 컴포넌트를 Deep Copy하지만, 참조 에셋(Mesh, Texture 등)은 복사하지 않고 참조만 복제합니다.
- Resources 폴더는 모든 에셋이 빌드에 포함되고 세밀한 언로드가 어려우므로, 모바일 프로젝트에서는 Addressables 전환이 권장됩니다.

직렬화와 로딩 과정에서 "무엇이 복사되고, 무엇이 공유되는가"를 구분할 수 있으면, Instantiate의 메모리 비용을 예측할 수 있습니다. 의존성 체인을 추적하면 불필요한 에셋 로딩도 식별할 수 있습니다.

<br>

이 글에서 다룬 직렬화, 로딩, Instantiate, 의존성 체인은 개별 에셋 단위의 동작입니다. 씬을 로드하면 씬에 배치된 모든 오브젝트의 역직렬화, 참조 에셋의 연쇄 로딩, 컴포넌트 초기화가 한꺼번에 일어나므로, 씬 전환이 게임에서 가장 큰 메모리 변동이 발생하는 시점입니다.
[Part 3](/dev/unity/UnityAsset-3/)에서 동기/비동기 씬 로딩, Additive 씬, 씬 전환 시 메모리 해제 패턴을 다룹니다.

에셋의 네이티브 메모리 사용 패턴은 [메모리 관리 (2)](/dev/unity/MemoryManagement-2/)에서, 동적 로드/해제 전략은 [메모리 관리 (3)](/dev/unity/MemoryManagement-3/)에서 확인할 수 있습니다.

<br>

---

**관련 글**
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)

**시리즈**
- [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)
- **Unity 에셋 시스템 (2) - Serialization과 Instantiation** (현재 글)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)

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
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
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
