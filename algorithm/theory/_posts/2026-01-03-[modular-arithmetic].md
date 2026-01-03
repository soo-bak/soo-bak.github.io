---
layout: single
title: "모듈러 연산(Modular Arithmetic)의 원리와 활용 - soo:bak"
date: "2026-01-03 14:00:00 +0900"
description: 나머지 연산의 성질, 모듈러 덧셈/뺄셈/곱셈, 거듭제곱, 역원 계산 방법을 다룹니다
---

## 모듈러 연산이란?

알고리듬 문제를 풀다 보면 "답을 $$10^9 + 7$$로 나눈 나머지를 출력하시오"라는 조건을 자주 보게 됩니다.

수가 너무 커지면 일반적인 자료형으로 표현할 수 없기 때문에, 나머지 연산을 활용하여 값을 관리하게 됩니다.

<br>

**모듈러 연산(Modular Arithmetic)**은 이러한 나머지 연산을 체계적으로 다루는 수학 분야입니다.

$$a \equiv b \pmod{m}$$

위 식은 $$a$$를 $$m$$으로 나눈 나머지가 $$b$$와 같다는 의미입니다.

<br>

예를 들어:
- $$17 \equiv 2 \pmod{5}$$ (17 = 5 * 3 + 2)
- $$-3 \equiv 4 \pmod{7}$$ (-3 = 7 * (-1) + 4)

---

## 기본 연산의 성질

모듈러 연산에서는 덧셈, 뺄셈, 곱셈에 대해 다음과 같은 분배 법칙이 성립합니다.

<br>

### 덧셈

$$(a + b) \mod m = ((a \mod m) + (b \mod m)) \mod m$$

```cpp
long long modAdd(long long a, long long b, long long m) {
  return ((a % m) + (b % m)) % m;
}
```

<br>

### 뺄셈

$$(a - b) \mod m = ((a \mod m) - (b \mod m) + m) \mod m$$

```cpp
long long modSub(long long a, long long b, long long m) {
  return ((a % m) - (b % m) + m) % m;
}
```

뺄셈의 경우 결과가 음수가 될 수 있으므로 $$m$$을 더해줍니다.

<br>

### 곱셈

$$(a \times b) \mod m = ((a \mod m) \times (b \mod m)) \mod m$$

```cpp
long long modMul(long long a, long long b, long long m) {
  return ((a % m) * (b % m)) % m;
}
```

곱셈에서는 오버플로우가 발생할 수 있으므로 `long long` 타입을 사용합니다.

---

## 모듈러 거듭제곱

$$a^n \mod m$$을 계산해야 할 때, $$n$$이 크다면 단순 반복으로는 시간이 오래 걸립니다.

분할 정복을 이용하면 $$O(\log n)$$ 시간에 계산할 수 있습니다.

<br>

### 원리

$$
a^n = \begin{cases}
1 & \text{if } n = 0 \\
(a^{n/2})^2 & \text{if } n \text{ is even} \\
a \times (a^{n/2})^2 & \text{if } n \text{ is odd}
\end{cases}
$$

지수를 절반씩 줄여가며 계산하므로 반복 횟수가 $$\log n$$에 비례합니다.

<br>

### 구현

```cpp
long long modPow(long long a, long long n, long long m) {
  long long result = 1;
  a %= m;

  while (n > 0) {
    if (n & 1) {
      result = result * a % m;
    }
    a = a * a % m;
    n >>= 1;
  }

  return result;
}
```

<br>

### 사용 예시

```cpp
// 2^10 mod 1000 = 1024 mod 1000 = 24
cout << modPow(2, 10, 1000) << "\n";  // 24

// 3^100 mod 1000000007
cout << modPow(3, 100, 1000000007) << "\n";
```

---

## 모듈러 역원

나눗셈의 경우 곱셈처럼 단순히 분배할 수 없습니다.

대신 **모듈러 역원**을 이용합니다.

<br>

$$a$$의 모듈러 역원 $$a^{-1}$$은 다음을 만족하는 수입니다:

$$a \times a^{-1} \equiv 1 \pmod{m}$$

역원이 존재하려면 $$\gcd(a, m) = 1$$이어야 합니다. 즉, $$a$$와 $$m$$이 서로소여야 합니다.

<br>

### 페르마의 소정리를 이용한 방법

$$m$$이 소수이고 $$\gcd(a, m) = 1$$일 때, 페르마의 소정리에 의해:

$$a^{m-1} \equiv 1 \pmod{m}$$

따라서:

$$a^{-1} \equiv a^{m-2} \pmod{m}$$

```cpp
long long modInverse(long long a, long long m) {
  return modPow(a, m - 2, m);
}
```

> 참고 : 이 방법은 $$m$$이 소수일 때만 사용할 수 있습니다.

<br>

### 확장 유클리드 알고리듬을 이용한 방법

$$m$$이 소수가 아닐 때는 확장 유클리드 알고리듬을 사용합니다.

```cpp
long long extGcd(long long a, long long b, long long& x, long long& y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }

  long long x1, y1;
  long long g = extGcd(b, a % b, x1, y1);
  x = y1;
  y = x1 - (a / b) * y1;

  return g;
}

long long modInverseExt(long long a, long long m) {
  long long x, y;
  long long g = extGcd(a, m, x, y);

  if (g != 1) return -1;  // 역원이 존재하지 않음

  return (x % m + m) % m;
}
```

> 참고 : [유클리드 호제법(Euclidean Algorithm)과 최대공약수 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

---

## 모듈러 나눗셈

역원을 이용하면 나눗셈을 곱셈으로 바꿀 수 있습니다.

$$\frac{a}{b} \mod m = a \times b^{-1} \mod m$$

```cpp
long long modDiv(long long a, long long b, long long m) {
  return modMul(a, modInverse(b, m), m);
}
```

---

## 실전 활용 예시

### 이항 계수 계산

조합 $$\binom{n}{r}$$을 큰 수에 대해 구할 때 모듈러 연산이 필수입니다.

$$\binom{n}{r} = \frac{n!}{r!(n-r)!}$$

팩토리얼과 그 역원을 미리 계산해두면 $$O(1)$$에 조합을 구할 수 있습니다.

```cpp
const long long MOD = 1000000007;
const int MAXN = 100001;

long long fact[MAXN], invFact[MAXN];

void precompute() {
  fact[0] = 1;
  for (int i = 1; i < MAXN; i++) {
    fact[i] = fact[i - 1] * i % MOD;
  }

  invFact[MAXN - 1] = modPow(fact[MAXN - 1], MOD - 2, MOD);
  for (int i = MAXN - 2; i >= 0; i--) {
    invFact[i] = invFact[i + 1] * (i + 1) % MOD;
  }
}

long long nCr(int n, int r) {
  if (r < 0 || r > n) return 0;
  return fact[n] * invFact[r] % MOD * invFact[n - r] % MOD;
}
```

<br>

### 문자열 해싱

문자열 비교를 빠르게 하기 위한 해시 계산에도 모듈러 연산이 사용됩니다.

```cpp
long long polyHash(const string& s, long long base, long long mod) {
  long long hash = 0;
  long long power = 1;

  for (char c : s) {
    hash = (hash + (c - 'a' + 1) * power) % mod;
    power = power * base % mod;
  }

  return hash;
}
```

---

## 자주 사용되는 MOD 값

알고리듬 문제에서 $$10^9 + 7$$이 가장 많이 사용됩니다.

이 값이 자주 쓰이는 이유는 다음과 같습니다:
- 소수이므로 페르마의 소정리를 적용할 수 있음
- `int` 범위의 두 수를 곱해도 `long long` 범위를 넘지 않음
- 외우기 쉬움

<br>

그 외에 $$10^9 + 9$$는 해싱에, $$998244353$$은 NTT(Number Theoretic Transform)에 자주 사용됩니다.

---

## 주의할 점

### 오버플로우

```cpp
// 위험: a * b가 long long 범위를 초과할 수 있음
long long result = a * b % m;

// 안전: 먼저 mod를 적용
long long result = (a % m) * (b % m) % m;
```

<br>

### 음수 처리

C++에서 음수를 양수로 나눈 나머지는 음수가 될 수 있습니다.

```cpp
int x = -7 % 5;  // -2

// 양수로 만들기
int x = ((-7 % 5) + 5) % 5;  // 3
```

<br>

### 역원 존재 조건

$$\gcd(a, m) = 1$$일 때만 역원이 존재합니다.

특히 $$m$$이 소수일 때는 $$a$$가 $$m$$의 배수가 아니면 항상 역원이 존재합니다.

---

## 마무리

모듈러 연산은 큰 수를 다루는 알고리듬 문제에서 기본이 되는 기법입니다.

덧셈, 뺄셈, 곱셈은 각각 mod를 분배할 수 있고, 나눗셈은 역원을 곱하는 방식으로 처리합니다.

거듭제곱은 분할 정복으로 $$O(\log n)$$에 계산할 수 있으며, 역원은 페르마의 소정리나 확장 유클리드 알고리듬으로 구합니다.

<br>

**관련 글**:
- [유클리드 호제법(Euclidean Algorithm)과 최대공약수 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

<br>

**관련 문제**:
- [[백준 11401] 이항 계수 3](https://www.acmicpc.net/problem/11401)
- [[백준 11444] 피보나치 수 6](https://www.acmicpc.net/problem/11444)
