---
layout: single
title: "확장 유클리드 알고리듬(Extended Euclidean Algorithm)의 원리와 구현 - soo:bak"
date: "2026-01-03 16:00:00 +0900"
description: GCD를 구하면서 베주 항등식의 계수를 함께 찾는 확장 유클리드 알고리듬의 원리와 활용을 다룹니다
---

## 확장 유클리드 알고리듬이란?

**확장 유클리드 알고리듬(Extended Euclidean Algorithm)**은 두 정수 $$a$$, $$b$$의 **최대공약수(GCD)**를 구하면서, 동시에 다음을 만족하는 정수 $$x$$, $$y$$를 찾습니다:

$$ax + by = \gcd(a, b)$$

<br>

이 식을 **베주 항등식(Bézout's Identity)**이라고 합니다.

<br>

**예시**

$$a = 30$$, $$b = 21$$

$$\gcd(30, 21) = 3$$

$$30 \times (-2) + 21 \times 3 = 3$$

따라서 $$x = -2$$, $$y = 3$$

<br>

## 알고리듬의 원리

<br>

### 기본 유클리드 알고리듬 복습

$$\gcd(a, b) = \gcd(b, a \mod b)$$

```
gcd(30, 21)
= gcd(21, 9)   // 30 mod 21 = 9
= gcd(9, 3)    // 21 mod 9 = 3
= gcd(3, 0)    // 9 mod 3 = 0
= 3
```

<br>

### 확장: 계수 역추적

유클리드 알고리듬의 각 단계에서 $$x$$, $$y$$를 역으로 계산합니다.

<br>

**기저 사례**: $$b = 0$$일 때

$$a \times 1 + 0 \times 0 = a = \gcd(a, 0)$$

따라서 $$x = 1$$, $$y = 0$$

<br>

**재귀 단계**:

$$\gcd(b, a \mod b) = bx_1 + (a \mod b)y_1$$을 알고 있을 때

$$a \mod b = a - \lfloor a/b \rfloor \times b$$이므로:

$$
\begin{align}
\gcd(a, b) &= bx_1 + (a - \lfloor a/b \rfloor b)y_1 \\
&= ay_1 + b(x_1 - \lfloor a/b \rfloor y_1)
\end{align}
$$

따라서:
- $$x = y_1$$
- $$y = x_1 - \lfloor a/b \rfloor y_1$$

<br>

## 구현

<br>

### 재귀 버전

```cpp
#include <bits/stdc++.h>
using namespace std;

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

int main() {
  long long a = 30, b = 21;
  long long x, y;

  long long g = extGcd(a, b, x, y);

  cout << "gcd(" << a << ", " << b << ") = " << g << "\n";
  cout << a << " * " << x << " + " << b << " * " << y << " = " << g << "\n";

  return 0;
}
```

**출력**:
```
gcd(30, 21) = 3
30 * -2 + 21 * 3 = 3
```

<br>

### 반복 버전

```cpp
long long extGcdIterative(long long a, long long b, long long& x, long long& y) {
  x = 1; y = 0;
  long long x1 = 0, y1 = 1;

  while (b != 0) {
    long long q = a / b;

    tie(x, x1) = make_tuple(x1, x - q * x1);
    tie(y, y1) = make_tuple(y1, y - q * y1);
    tie(a, b) = make_tuple(b, a - q * b);
  }

  return a;
}
```

<br>

### 구조체 반환 버전

```cpp
struct ExtGcdResult {
  long long g, x, y;
};

ExtGcdResult extGcd(long long a, long long b) {
  if (b == 0) {
    return {a, 1, 0};
  }

  auto [g, x1, y1] = extGcd(b, a % b);
  return {g, y1, x1 - (a / b) * y1};
}
```

<br>

## 시간 복잡도

<br>

- **시간**: $$O(\log(\min(a, b)))$$
- **공간**: $$O(\log(\min(a, b)))$$ (재귀), $$O(1)$$ (반복)

<br>

## 활용

<br>

### 1. 모듈러 역원

$$a^{-1} \mod m$$ 구하기:

$$ax \equiv 1 \pmod{m}$$

이는 $$ax + my = 1$$을 만족하는 $$x$$ 찾기와 같습니다.

```cpp
long long modInverse(long long a, long long m) {
  long long x, y;
  long long g = extGcd(a, m, x, y);

  if (g != 1) {
    return -1;  // 역원 없음 (a와 m이 서로소가 아님)
  }

  return (x % m + m) % m;  // 양수로 변환
}
```

<br>

### 2. 선형 디오판틴 방정식

$$ax + by = c$$의 정수해 찾기

해가 존재할 조건: $$\gcd(a, b) \mid c$$

```cpp
bool solveDiophantine(long long a, long long b, long long c,
                      long long& x, long long& y) {
  long long g = extGcd(a, b, x, y);

  if (c % g != 0) {
    return false;  // 해 없음
  }

  // 특수해
  x *= c / g;
  y *= c / g;

  return true;
}
```

<br>

**일반해**:

특수해 $$(x_0, y_0)$$가 있으면, 모든 해는:

$$
x = x_0 + \frac{b}{\gcd(a,b)} t, \quad
y = y_0 - \frac{a}{\gcd(a,b)} t
$$

<br>

### 3. 중국인의 나머지 정리 (CRT)

연립 합동식 풀기:

$$
\begin{cases}
x \equiv a_1 \pmod{m_1} \\
x \equiv a_2 \pmod{m_2}
\end{cases}
$$

```cpp
pair<long long, long long> crt(long long a1, long long m1,
                                long long a2, long long m2) {
  long long p, q;
  long long g = extGcd(m1, m2, p, q);

  if ((a2 - a1) % g != 0) {
    return {-1, -1};  // 해 없음
  }

  long long lcm = m1 / g * m2;
  long long ans = a1 + m1 * ((a2 - a1) / g * p % (m2 / g));
  ans = ((ans % lcm) + lcm) % lcm;

  return {ans, lcm};
}
```

<br>

### 4. 분수의 기약 표현

```cpp
pair<long long, long long> reduceFraction(long long num, long long den) {
  long long g = __gcd(abs(num), abs(den));
  if (den < 0) {
    num = -num;
    den = -den;
  }
  return {num / g, den / g};
}
```

<br>

## 예제: 단계별 추적

<br>

$$\gcd(35, 15)$$의 계수 찾기:

```
단계 1: gcd(35, 15)
  35 = 15 * 2 + 5

단계 2: gcd(15, 5)
  15 = 5 * 3 + 0

단계 3: gcd(5, 0) = 5
  x = 1, y = 0
  5 * 1 + 0 * 0 = 5 ✓

역추적 단계 2:
  x = 0, y = 1 - 3*0 = 1
  15 * 0 + 5 * 1 = 5 ✓

역추적 단계 1:
  x = 1, y = 0 - 2*1 = -2
  35 * 1 + 15 * (-2) = 5 ✓
```

**결과**: $$35 \times 1 + 15 \times (-2) = 5$$

<br>

## 주의사항

<br>

**1. 해의 유일성**

베주 계수는 유일하지 않습니다:

$$35 \times 1 + 15 \times (-2) = 5$$

$$35 \times (-2) + 15 \times 5 = 5$$

모두 올바른 해입니다.

<br>

**2. 음수 입력**

$$a$$나 $$b$$가 음수일 수 있으므로 적절히 처리:

```cpp
// 필요시 절댓값 사용
long long g = extGcd(abs(a), abs(b), x, y);
if (a < 0) x = -x;
if (b < 0) y = -y;
```

<br>

**3. 오버플로우**

중간 계산에서 곱셈이 발생하므로 `long long` 사용 권장

<br>

## 마무리

확장 유클리드 알고리듬은 GCD와 함께 베주 계수를 찾는 강력한 도구입니다.

<br>

**핵심 포인트**
- **베주 항등식**: $$ax + by = \gcd(a, b)$$
- **계수 계산**: $$x = y_1$$, $$y = x_1 - \lfloor a/b \rfloor y_1$$
- **시간 복잡도**: $$O(\log(\min(a, b)))$$
- **활용**: 모듈러 역원, 디오판틴 방정식, CRT

<br>

### 관련 글
- [유클리드 알고리듬(Euclidean Algorithm) - soo:bak](https://soo-bak.github.io/algorithm/theory/euclidean-algorithm/)
- [모듈러 연산(Modular Arithmetic) - soo:bak](https://soo-bak.github.io/algorithm/theory/modular-arithmetic/)

<br>

### 관련 문제
- [[백준 3955] 캔디 분배](https://www.acmicpc.net/problem/3955)
- [[백준 14565] 역원(Inverse) 구하기](https://www.acmicpc.net/problem/14565)

