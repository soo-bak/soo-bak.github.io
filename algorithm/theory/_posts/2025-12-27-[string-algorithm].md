---
layout: single
title: "문자열 알고리즘 - 패턴 매칭과 해싱 - soo:bak"
date: "2025-12-27 01:00:00 +0900"
description: 문자열 탐색의 기본 개념부터 KMP 알고리즘, 라빈-카프 해싱까지 문자열 알고리즘의 핵심 원리와 구현 방법을 설명합니다.
---

## 문자열 알고리즘이란?

**문자열 알고리즘**은 텍스트 데이터를 효율적으로 처리하기 위한 알고리즘입니다.

<br>
문자열 처리는 검색 엔진, 텍스트 편집기, DNA 서열 분석, 데이터 압축 등 다양한 분야에서 핵심적인 역할을 합니다.

<br>
문자열 알고리즘의 대표적인 문제는 **패턴 매칭(Pattern Matching)** 입니다.

긴 텍스트에서 특정 패턴이 등장하는 위치를 찾는 것으로,

단순한 방법부터 고급 알고리즘까지 다양한 접근법이 존재합니다.

<br>

---

<br>

## 단순 패턴 매칭 (Naive Algorithm)

가장 직관적인 방법은 텍스트의 모든 위치에서 패턴을 하나씩 비교하는 것입니다.

<br>

### 동작 원리

텍스트 `T`와 패턴 `P`가 주어졌을 때:

1. 텍스트의 각 위치 `i`에서 시작
2. 패턴의 모든 문자를 순서대로 비교
3. 모든 문자가 일치하면 매칭 성공
4. 불일치 시 다음 위치로 이동

<br>

### 예시

```
텍스트: ABABDABACDABABCABAB
패턴:   ABABCABAB

위치 0: ABABD... vs ABABC... → 4번째에서 불일치
위치 1: BABDA... vs ABABC... → 0번째에서 불일치
...
위치 10: ABABCABAB vs ABABCABAB → 매칭 성공!
```

<br>

### 시간 복잡도

텍스트 길이 `n`, 패턴 길이 `m`일 때 최악의 경우 **O(n × m)** 입니다.

<br>
예를 들어, 텍스트가 `AAAAAAAAAA`이고 패턴이 `AAAAB`인 경우,

매 위치에서 거의 모든 문자를 비교해야 합니다.

<br>

---

<br>

## KMP 알고리즘

**KMP(Knuth-Morris-Pratt) 알고리즘**은 불일치가 발생했을 때 이미 비교한 정보를 활용하여 불필요한 비교를 건너뜁니다.

<br>

### 핵심 아이디어: 실패 함수 (Failure Function)

패턴 내에서 **접두사(Prefix)와 접미사(Suffix)가 일치하는 최대 길이**를 미리 계산합니다.

<br>
이를 **실패 함수** 또는 **부분 일치 테이블**이라고 합니다.

<br>

### 실패 함수 예시

패턴 `ABABCABAB`의 실패 함수:

```
인덱스:  0  1  2  3  4  5  6  7  8
패턴:    A  B  A  B  C  A  B  A  B
실패값:  0  0  1  2  0  1  2  3  4
```

<br>
`실패값[8] = 4`의 의미:

`ABABCABAB`의 처음 9글자에서 접두사와 접미사가 일치하는 최대 길이가 4입니다.

즉, `ABAB` (앞 4글자) = `ABAB` (뒤 4글자)

<br>

### KMP의 동작

불일치 발생 시, 실패 함수를 이용해 패턴을 적절한 위치로 이동합니다.

<br>
이미 일치한 부분의 접두사-접미사 관계를 활용하므로,

텍스트의 포인터는 뒤로 돌아가지 않습니다.

<br>

### 시간 복잡도

실패 함수 계산: **O(m)**

패턴 매칭: **O(n)**

전체: **O(n + m)**

<br>

---

<br>

## 라빈-카프 알고리즘 (해싱)

**라빈-카프(Rabin-Karp) 알고리즘**은 해시 함수를 이용하여 패턴 매칭을 수행합니다.

<br>

### 핵심 아이디어: 롤링 해시

문자열을 숫자(해시값)로 변환하여 비교합니다.

<br>
텍스트의 연속된 부분 문자열의 해시값을 효율적으로 계산하기 위해

**롤링 해시(Rolling Hash)** 기법을 사용합니다.

<br>

### 롤링 해시의 원리

문자열 `S = s₀s₁s₂...sₘ₋₁`의 해시값:

```
H(S) = s₀ × dᵐ⁻¹ + s₁ × dᵐ⁻² + ... + sₘ₋₁ × d⁰ (mod q)
```

<br>
여기서 `d`는 기수(보통 문자 종류 수), `q`는 큰 소수입니다.

<br>
다음 위치의 해시값은 이전 해시값을 이용해 **O(1)** 에 계산됩니다:

```
H(S[i+1...i+m]) = (H(S[i...i+m-1]) - s[i] × dᵐ⁻¹) × d + s[i+m]
```

<br>

### 시간 복잡도

평균: **O(n + m)**

최악 (해시 충돌이 많은 경우): **O(n × m)**

<br>

---

<br>

## 문자열 알고리즘 비교

| 알고리즘 | 전처리 | 탐색 | 특징 |
|---------|--------|------|------|
| 단순 매칭 | - | O(nm) | 구현 간단 |
| KMP | O(m) | O(n) | 안정적인 성능 |
| 라빈-카프 | O(m) | O(n) 평균 | 다중 패턴에 유리 |

<br>
단일 패턴 매칭에는 **KMP**가 안정적입니다.

여러 패턴을 동시에 찾거나, 해시 기반 비교가 필요한 경우 **라빈-카프**가 유용합니다.

<br>

---

<br>

## 기본 구현 예시

### KMP 알고리즘 (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> getFailure(const string& pattern) {
    int m = pattern.length();
    vector<int> fail(m, 0);
    int j = 0;

    for (int i = 1; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j])
            j = fail[j - 1];
        if (pattern[i] == pattern[j])
            fail[i] = ++j;
    }
    return fail;
}

vector<int> kmp(const string& text, const string& pattern) {
    vector<int> result;
    vector<int> fail = getFailure(pattern);
    int n = text.length(), m = pattern.length();
    int j = 0;

    for (int i = 0; i < n; i++) {
        while (j > 0 && text[i] != pattern[j])
            j = fail[j - 1];
        if (text[i] == pattern[j]) {
            if (j == m - 1) {
                result.push_back(i - m + 1);
                j = fail[j];
            } else {
                j++;
            }
        }
    }
    return result;
}
```

<br>

---

<br>

## 관련 문제 유형

문자열 알고리즘은 다음과 같은 문제에서 활용됩니다:

- 부분 문자열 찾기
- 문자열 내 패턴 등장 횟수 세기
- 가장 긴 공통 부분 문자열
- 문자열 압축 및 인코딩
- 회문(Palindrome) 판별

<br>

