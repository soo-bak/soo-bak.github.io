---
layout: single
title: "Middle-Square 방식 난수 생성 알고리듬의 원리와 한계 - soo:bak"
date: "2025-04-22 22:03:00 +0900"
description: 중간 네 자리를 추출하는 방식으로 난수를 생성하는 Middle-Square 메서드 기법의 작동 방식과 알고리듬적 원리, 그리고 그 한계에 대해 설명한 글
---

## Middle-Square 방식이란?

**Middle-Square 방식**은 난수 생성 알고리듬 중 하나로, 간단한 구현 방식 때문에 한때 실제 시스템에서도 사용되었던 기법입니다.<br>
<br>
기본 아이디어는 다음과 같습니다:
- 주어진 수를 제곱한 뒤,
- 중간의 일정 자릿수를 추출하여
- 그 값을 다음 수로 사용하는 방식입니다.

이 과정을 반복하면서 새로운 수열을 만들어냅니다.

---

## 알고리듬 구조

Middle-Square 방식은 입력값(예: 4자리 수)을 다음과 같은 수식으로 변환합니다:

$$
(x_{n+1} = \left( \frac{x_n^2}{10^k} \right) \mod 10^d)
$$

- $$x_n$$: 현재 수
- $$x_n^2$$: 제곱한 수
- $$k$$: 앞뒤 자릿수를 버리기 위해 나누는 자릿수 (중간을 추출)
- $$d$$: 최종적으로 남길 자릿수 수 (보통 4자리)

예를 들어, $$x = 1234$$ 라면:<br>
- $$x^2 = 1522756$$ 에서,
- 가운데 4자리인 $$5227$$을 추출해 다음 수로 사용합니다.

이러한 방식은 난수처럼 보이는 수열을 만들어내지만, 실제로는 확정적인 규칙에 따라 진행되는 순열 구조를 가집니다.

---

## C++ 코드 예시

```cpp
int next(int x) {
  return (x * x / 100) % 10000; // 중간 4자리 추출
}

int countUntilCycle(int start) {
  bool visited[10000] = {false};
  int cnt = 0;
  while (!visited[start]) {
    visited[start] = true;
    start = next(start);
    cnt++;
  }
  return cnt;
}
```

이 코드는 어떤 수가 처음 중복되기 전까지 몇 개의 수가 생성되는지를 계산합니다.

---

## 수학적 특징과 반복 구조

이 방식은 항상 **중복 발생**으로 인해 수열이 순환하게 됩니다.<br>
그 이유는 가능한 값의 개수가 유한하기 때문입니다. 4자리 수의 경우:

- 가능한 수의 개수는 $$10,000$$개 (0000부터 9999까지)
- 따라서 10,000번 이상 반복하면 반드시 중복이 발생합니다.

이것은 **비둘기집 원리**에 의해 보장됩니다.<br>

> 참고 : [비둘기집 원리(Pigeonhole Principle)의 직관과 알고리듬 문제에서의 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/pigeonhole-principle)

<br>

또한, 같은 수가 두 번 등장하면 이후 수열은 완전히 동일하게 반복됩니다.<br>
즉, $$a_n = a_m$$이면 이후 수열은 $$a_{n+1} = a_{m+1}, a_{n+2} = a_{m+2}, \dots$$ 와 같이 진행됩니다.

이 구조는 일반적인 `순열 반복 구조(permutation cycle)`로 이해할 수 있으며, 초기값에 따라 길이와 반복 구간이 달라질 수 있습니다.


> 참고 : [순열 반복 구조(Permutation Cycle)의 개념과 알고리듬적 활용 - soo:bak](https://soo-bak.github.io/algorithm/theory/middle-square-algorithm/)


---

## 장점과 한계

### 장점
- 구현이 매우 단순하고 직관적입니다.
- 디버깅, 알고리듬 수업용 예시로 사용하기 적합합니다.

### 한계
- 생성되는 수열의 주기가 매우 짧습니다.
- 특정 입력에 대해 0으로 수렴하거나 아주 짧은 순환에 빠질 수 있습니다.
- 현대 난수 생성기 기준에서는 예측 가능성과 주기성 때문에 보안/통계적 사용에 적합하지 않습니다.

예를 들어:
- `0000` → 항상 `0`
- `6100` → `2100` → `4100` → `8100` → `6100`처럼 4개 길이의 순환 발생

---

## 실제 활용 사례

Middle-Square 방식은 현재 실무 시스템에서는 사용되지 않지만, 알고리듬 학습이나 다음과 같은 목적으로 활용됩니다:
- 난수 생성의 구조적 한계를 보여주는 학습 용도
- 사이클 탐지 문제, 방문 체크 기반 순열 분석 등 문제 풀이에서 연습 예시로 사용
<br>

---

## 마무리

Middle-Square 방식은 단순한 수학적 아이디어로부터 시작된 고전적인 난수 생성 기법입니다.<br>
<br>
비록 현대적인 기준에서는 실용성이 떨어지지만,<br>
<br>
수열의 반복 구조, 순환 패턴, 입력과 출력 간의 관계를 이해하는 것에 큰 도움이 됩니다.<br>
<br>
또한, **중복 발생의 원리**, **순환 수열의 형태**, **비둘기집 원리의 응용** 등을 함께 익힐 수 있는 기법입니다.

<br>
> 관련 문제: [[백준 6500] 랜덤 숫자 만들기 (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/random-number-generation-45/)
