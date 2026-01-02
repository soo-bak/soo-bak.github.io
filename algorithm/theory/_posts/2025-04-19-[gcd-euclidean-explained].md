---
layout: single
title: "유클리드 호제법(Euclidean Algorithm)과 최대공약수 - soo:bak"
date: "2025-04-19 01:31:00 +0900"
description: 두 수의 최대공약수를 효율적으로 구하는 유클리드 호제법의 원리, 증명, 구현 방법, 시간 복잡도, 그리고 다양한 활용 예시를 다룹니다
---

## 유클리드 호제법이란?

두 자연수 `1071`과 `1029`의 최대공약수를 구해야 한다고 가정해보겠습니다.

모든 약수를 일일이 나열하여 비교하는 방법은 수가 커질수록 비효율적입니다.

예를 들어, 수가 `1,000,000,007`과 `1,000,000,009`처럼 매우 크다면 약수를 일일이 나열하는 것은 현실적으로 불가능합니다.

<br>

**유클리드 호제법(Euclidean Algorithm)**은 이러한 문제를 해결하는 효율적인 알고리듬입니다.

기원전 300년경 고대 그리스 수학자 유클리드의 저서 『원론』에 소개된 이 방법은, 나눗셈의 나머지를 이용하여 두 수의 **최대공약수(Greatest Common Divisor, GCD)**를 빠르게 구합니다.

---

## 최대공약수(GCD)

두 자연수 $$a$$, $$b$$ 에 대해 공통된 약수 중 가장 큰 값을 **최대공약수**라고 합니다.

예를 들어, $$a = 24$$, $$b = 36$$이라면,
- `24`의 약수: `1, 2, 3, 4, 6, 8, 12, 24`
- `36`의 약수: `1, 2, 3, 4, 6, 9, 12, 18, 36`
- 공통 약수: `1, 2, 3, 4, 6, 12`

따라서 $$\gcd(24, 36) = 12$$입니다.

<br>

최대공약수는 다음과 같은 성질을 가집니다:
- $$\gcd(a, b) = \gcd(b, a)$$ (교환 법칙)
- $$\gcd(a, 0) = a$$ (어떤 수와 0의 최대공약수는 그 수 자신)
- $$\gcd(a, b) = \gcd(a - b, b)$$ ($$a > b$$일 때)

---

## 유클리드 호제법의 원리

유클리드 호제법의 핵심은 다음과 같은 성질입니다:

$$
\gcd(a, b) = \gcd(b, a \bmod b) \quad (b \neq 0)
$$

즉, 큰 수를 작은 수로 나눈 나머지를 이용하여 문제의 크기를 반복적으로 줄여나가며, 나머지가 `0`이 되는 순간 최대공약수를 얻게 됩니다.

<br>

### 단계별 예시

$$\gcd(48, 18)$$을 구하는 과정:

1. $$\gcd(48, 18)$$
   - $$48 = 18 \times 2 + 12$$
   - $$\gcd(48, 18) = \gcd(18, 12)$$

2. $$\gcd(18, 12)$$
   - $$18 = 12 \times 1 + 6$$
   - $$\gcd(18, 12) = \gcd(12, 6)$$

3. $$\gcd(12, 6)$$
   - $$12 = 6 \times 2 + 0$$
   - $$\gcd(12, 6) = \gcd(6, 0) = 6$$

따라서 $$\gcd(48, 18) = 6$$입니다.

<br>

각 단계마다 나머지가 이전 단계의 나누는 수보다 작아지므로, 점점 문제가 단순해집니다.

---

## 수학적 증명

두 정수 $$a$$, $$b$$에 대해 나눗셈을 수행하면 다음과 같이 표현할 수 있습니다:

$$
a = bq + r \quad (0 \leq r < b)
$$

여기서 $$q$$는 몫, $$r = a \bmod b$$는 나머지입니다.

<br>

이제 $$\gcd(a, b) = \gcd(b, r)$$임을 증명하겠습니다.

<br>

### 1) $$\gcd(a, b)$$는 $$r$$의 약수이다

$$d = \gcd(a, b)$$라고 하면, $$d$$는 $$a$$와 $$b$$의 공약수입니다.

즉, $$a = dk_1$$, $$b = dk_2$$로 나타낼 수 있습니다.

$$a = bq + r$$에서 $$r = a - bq = dk_1 - dk_2 q = d(k_1 - k_2 q)$$이므로,

$$d$$는 $$r$$의 약수이기도 합니다.

<br>

### 2) $$\gcd(b, r)$$은 $$a$$의 약수이다

반대로, $$d' = \gcd(b, r)$$이라고 하면, $$b = d'm_1$$, $$r = d'm_2$$로 나타낼 수 있습니다.

$$a = bq + r = d'm_1 q + d'm_2 = d'(m_1 q + m_2)$$이므로,

$$d'$$은 $$a$$의 약수이기도 합니다.

<br>

### 결론

위 두 사실로부터 $$\gcd(a, b)$$와 $$\gcd(b, r)$$은 서로 같은 수의 공약수를 가지며, 따라서:

$$
\gcd(a, b) = \gcd(b, r)
$$

이 성립합니다.

---

## 구현

### 재귀 구현

수학적 정의를 그대로 코드로 옮긴 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int gcd(int a, int b) {
  // 기저 조건: b가 0이면 a가 최대공약수
  if (b == 0) return a;
  
  // 재귀 호출: gcd(b, a % b)
  return gcd(b, a % b);
}

int main() {
  int a, b;
  cin >> a >> b;
  cout << gcd(a, b) << "\n";
  return 0;
}
```

**장점**:
- 코드가 간결하고 직관적
- 수학적 정의와 일치하여 이해하기 쉬움

**단점**:
- 재귀 호출로 인한 함수 호출 오버헤드 발생
- 입력이 매우 큰 경우 스택 오버플로우 가능성 (실제로는 거의 발생하지 않음)

<br>

### 반복 구현

재귀 호출 대신 반복문을 사용한 형태입니다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int gcd(int a, int b) {
  // b가 0이 될 때까지 반복
  while (b != 0) {
    int r = a % b;  // 나머지 계산
    a = b;          // a를 b로 갱신
    b = r;          // b를 나머지로 갱신
  }
  return a;  // b가 0이 되면 a가 최대공약수
}

int main() {
  int a, b;
  cin >> a >> b;
  cout << gcd(a, b) << "\n";
  return 0;
}
```

**장점**:
- 함수 호출 오버헤드가 없어 미세하게 더 빠름
- 스택 오버플로우 걱정 없음

**단점**:
- 재귀 버전에 비해 코드가 약간 더 김

<br>

실전에서는 두 방법 모두 충분히 빠르므로, 선호하는 스타일에 따라 선택하면 됩니다.

C++ 표준 라이브러리에서는 `<algorithm>` 헤더의 `__gcd(a, b)` 또는 C++17부터 제공되는 `std::gcd(a, b)`를 사용할 수도 있습니다.

---

## 시간 복잡도

유클리드 호제법의 시간 복잡도는 다음과 같습니다:

$$
O(\log \min(a, b))
$$

각 단계에서 나머지는 이전 나누는 수보다 반드시 작으므로, 문제의 크기가 빠르게 줄어듭니다.

<br>

### 최악의 경우

최악의 경우는 **피보나치 수열의 연속된 두 항**을 입력으로 받을 때입니다.

예를 들어, $$\gcd(F_n, F_{n-1})$$을 계산할 때:

$$
\gcd(21, 13) \\
\gcd(13, 8) \\
\gcd(8, 5) \\
\gcd(5, 3) \\
\gcd(3, 2) \\
\gcd(2, 1) \\
\gcd(1, 0)
$$

이 경우에도 피보나치 수는 지수적으로 증가하므로, 전체 반복 횟수는 입력 값의 자릿수에 비례합니다.

따라서 최악의 경우에도 여전히 $$O(\log n)$$ 복잡도를 유지합니다.

<br>

### 공간 복잡도

- 재귀 구현: $$O(\log n)$$ (재귀 스택)
- 반복 구현: $$O(1)$$

---

## 유클리드 호제법의 활용

### 1) 최소공배수(LCM) 계산

두 수의 최소공배수는 다음 공식으로 구할 수 있습니다:

$$
\text{lcm}(a, b) = \frac{a \times b}{\gcd(a, b)}
$$

```cpp
long long lcm(long long a, long long b) {
  return a / gcd(a, b) * b;  // 오버플로우 방지를 위해 나눗셈을 먼저 수행
}
```

주의: $$a \times b$$를 먼저 계산하면 정수 오버플로우가 발생할 수 있으므로, $$a / \gcd(a, b)$$를 먼저 계산한 후 $$b$$를 곱합니다.

<br>

### 2) 분수의 기약분수 변환

분자와 분모의 최대공약수로 나누면 기약분수를 만들 수 있습니다.

```cpp
void reduceFraction(int& numerator, int& denominator) {
  int g = gcd(numerator, denominator);
  numerator /= g;
  denominator /= g;
}
```

> 참고 : [기약 분수(irreducible fraction)의 알고리듬적 접근 - soo:bak](https://soo-bak.github.io/algorithm/theory/irreducible-fraction/)

<br>

### 3) 서로소 판별

두 수의 최대공약수가 `1`이면 두 수는 서로소입니다.

```cpp
bool areCoprime(int a, int b) {
  return gcd(a, b) == 1;
}
```

서로소 관계는 정수론, 암호학, 조합론 등에서 중요하게 사용됩니다.

<br>

### 4) 확장 유클리드 호제법

유클리드 호제법을 확장하면 $$ax + by = \gcd(a, b)$$를 만족하는 정수 $$x$$, $$y$$를 구할 수 있습니다.

이는 모듈러 역원 계산, 디오판토스 방정식 해결 등에 활용됩니다.

<br>

### 5) 다수의 수의 최대공약수

여러 수의 최대공약수는 순차적으로 계산할 수 있습니다:

$$
\gcd(a_1, a_2, a_3, \ldots, a_n) = \gcd(\gcd(\cdots\gcd(\gcd(a_1, a_2), a_3), \ldots), a_n)
$$

```cpp
int gcdMultiple(vector<int>& arr) {
  int result = arr[0];
  for (int i = 1; i < arr.size(); i++) {
    result = gcd(result, arr[i]);
    if (result == 1) break;  // 더 이상 줄어들 수 없음
  }
  return result;
}
```

---

## 실전 예제: 최소공배수 구하기

### 문제

두 자연수 $$A$$, $$B$$가 주어졌을 때, 최소공배수를 구하는 프로그램을 작성하시오.

- 제약: $$1 \leq A, B \leq 10^9$$
- 입력: 두 정수 $$A$$, $$B$$
- 출력: 최소공배수

<br>

### 접근법

최소공배수는 두 수의 곱을 최대공약수로 나누어 구할 수 있습니다.

단, 두 수의 곱이 `long long` 범위를 초과할 수 있으므로, 먼저 한 수를 최대공약수로 나눈 후 다른 수를 곱합니다.

<br>

### 구현

```cpp
#include <bits/stdc++.h>
using namespace std;

// 유클리드 호제법으로 최대공약수 계산
long long gcd(long long a, long long b) {
  while (b != 0) {
    long long r = a % b;
    a = b;
    b = r;
  }
  return a;
}

// 최소공배수 계산
long long lcm(long long a, long long b) {
  return a / gcd(a, b) * b;  // 오버플로우 방지
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);
  
  long long a, b;
  cin >> a >> b;
  
  cout << lcm(a, b) << "\n";
  
  return 0;
}
```

<br>

### 시간 복잡도

- GCD 계산: $$O(\log \min(a, b))$$
- LCM 계산: $$O(1)$$ (GCD 이후 나눗셈과 곱셈)
- **전체**: $$O(\log \min(a, b))$$

---

## 마무리

유클리드 호제법은 2000년 이상의 역사를 가진 알고리듬이지만, 현대 컴퓨터 과학에서도 여전히 중요하게 사용되고 있습니다.

나머지 연산을 통해 문제의 크기를 빠르게 줄여나가는 구조는 단순하지만 매우 효율적입니다.

<br>

최대공약수는 정수론, 조합론, 암호학 등 다양한 분야에서 기초가 되는 개념이며,

유클리드 호제법은 이를 효율적으로 계산하는 가장 기본적이면서도 강력한 방법입니다.


알고리듬 문제에서 최대공약수나 최소공배수 계산이 필요한 경우, 유클리드 호제법의 활용을 떠올리면 큰 도움이 됩니다.

<br>

**관련 글**:
- [기약 분수(irreducible fraction)의 알고리듬적 접근 - soo:bak](https://soo-bak.github.io/algorithm/theory/irreducible-fraction/)

<br>

**관련 문제**:
- [[백준 1934] 최소공배수](https://soo-bak.github.io/algorithm/boj/lcm-52/)
- [[백준 5347] LCM](https://soo-bak.github.io/algorithm/boj/lcmMultiple-12/)
- [[백준 1735] 분수 합](https://soo-bak.github.io/algorithm/boj/fractionSum-53/)
- [[백준 29196] 소수가 아닌 수 2](https://soo-bak.github.io/algorithm/boj/NotFractionNumberTwo-12/)
