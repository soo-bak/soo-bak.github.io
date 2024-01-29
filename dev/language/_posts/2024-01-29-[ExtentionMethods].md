---
layout: single
title: "C#의 확장 메서드(Extension Methods) - soo:bak"
date: "2024-01-29 22:03:00 +0900"
---
<br>

## 확장 메서드(Extension Methods)
확장 메서드는 기존 타입의 소스 코드를 변경하지 않고도, 해당 타입에 새로운 메서드를 추가할 수 있도록 해준다.<br>
<br>
이는 '개방/폐쇄 원칙 (Open/Closed Principle)` 을 따르는 매우 우아한 방법들 중 하나다.<br>
<br>
즉, 소프트웨어 개체(클래스, 모듈, 함수 등)는 확장에는 열려 있어야 하지만, 변경에는 닫혀 있어야 한다는 원칙을 실현할 수 있다.<br>
<br>
<br>
확장 메서드를 작성하기 위한 조건은 간단하다.<br>
<br>
- 메서드는 정적 클래스 안에 정의되어야 한다.<br>
<br>
- 메서드 자체도 정적이어야 한다.<br>
<br>
- 첫 번쨰 매개변수에는 `this` 키워드를 사용하여, 확장하고자 하는 타입을 지정해야 한다.<br>
<br><br><br>

## 확장 메서드 작성 예시
가령, `IEnumerable<T>` 인터페이스에 대한 확장 메서드를 작성하여 컬렉션의 모든 원소를 문자열로 결합하는 기능을 추가하고자 한다면, 다음과 같이 코드를 작성할 수 있다.<br>
<br>
```c#
public static class EnumerableExtensions {
  public static string StringJoin<T>(this IEnumerable<T> collection, string seperator) {
    return string.Join(seperator, collections);
  }
}
```
<br>
이 확장 메서드를 사용하면, 어떤 `IEnumerable<T>` 타입의 컬렉션이든 간편하게 원소들을 문자열로 결합할 수 있다.<br>
<br><br><br>

## 확장 메서드의 사용
확장 메서드를 사용하괴 위해서는 해당 메서드가 정의된 정적 클래스를 포함하고 있는 명칭 공간을 `using` 지시어를 통해 포함시켜야 한다.<br>
<br>
그 후, 기존 타입의 인스턴스에 대해 마치 인스턴스 메서드인 것 처럼 확장 메서드를 호출할 수 있다.<br>
<br>
```c#
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var result = numbers.StringJoin(", ");
Console.WriteLine(result);
// 출력: 1, 2, 3, 4, 5
```
<br><br><br>

## 확장 메서드와 LINQ
확장 메서드는 단순히 기존 타입에 메서드를 추가하는 것 이상의 가치를 제공한다.<br>
<br>
예를 들어, `LINQ (Language Integrated Query)` 는 확장 메서드 활용의 좋은 사례 중 하나이다.<br>
<br>
`LINQ` 는 `IEnumerable<T>` 및 `IQueryable<T>` 타입에 대한 많은 확장 메서드를 제공하여, 컬렉션에 대한 강력하고 선언적인 쿼리 기능을 가능하게 한다.<br>
<br><br>

### LINQ 확장 메서드 예시
```c#
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// 홀수만 필터링
var oddNumbers = numbers.Where(n => n % 2 != 0);

// 각 원소를 제곱
var squaredNumbers = numbers.Select(n => n * n);

// 원소 정렬
var sortedNumbers = numbres.OrderByDescending(n => n);

// 합계 계산
var sumOfNumbers = numbers.Sum();
```
<br>
여기서, `Where`, `Select`, `OrderByDescending`, `Sum` 등은 모두 `IEnumerable<T>` 에 대한 확장 메서드이다.<br>
<br>
이들 메서드는 각각 필터링, 변환, 정렬, 집계 등의 기능을 수행한다.<br>
<br><br>

### LINQ 의 지연 실행 (Lazy Evaluation)
`LINQ` 확장 메서드의 중요한 특징 중 하나는, 대부분의 쿼리 연산이 지연 실행(Lazy Evaluation)을 사용한다는 것이다.<br>
<br>
즉, 실제로 쿼리의 결과가 필요할 때 까지 쿼리 실행이 지연된다.<br>
<br>
예를 들어, `Where` 메서드를 사용해 컬렉션을 필터링하는 경우, 필터링된 원소가 실제로 열거될 때까지 쿼리가 실행되지 않는다.<br>
<br>
```c#
var filteredNumbers = numbers.Where(n => n > 5);
// 이 시점에는 쿼리가 실행되지 않음

foreach (var num in filteredNumbers) {
  Console.WriteLine(num); // 여기서 실제로 Where 쿼리가 실행됨
}

```
<br>
이 지연 실행 방식은 필요한 데이터만 처리하게 하여, 메모리 사용량과 성능을 최적화할 수 있게 한다.<br>
<br><br>

### LINQ 와 익명 타입
`LINQ` 쿼리에서는 종종 익명 타입을 사용하여 새로운 데이터 형태를 쉽게 생성하고 반환한다.<br>
<br>
예를 들어, 다음 `LINQ` 쿼리는 각 숫자와 그 제곱 값을 포함하는 새로운 익명의 컬렉션을 생성한다.<br>
<br>
```c#
var numberInfo = numbers.Select(n => new { Number = n, Squared = n * n });

foreach (var item in numberInfo) {
  Console.WriteLine($"Number: {item.Number}, Squared: {item.Squared}");
}
```
<br>
여기서 `new { Number = n, Squared = n * n}` 은 익명 타입을 사용하여 각 숫자와 그 제곱 값을 쌍으로 묶는 익명 객체를 생성한다.<br>
<br><br>

### LINQ 와 함수형 프로그래밍
`LINQ` 는 함수형 프로그래밍의 개념을 `C#` 에 가져온다. <br>
<br>
`Where` , `Select` , `Aggregate` 와 같은 메서드들은 `고차 함수(Higher-Order Functions)` 로, 다른 함수(예: 람다 식)를 매개변수로 받아 데이터를 변환하고 조작한다.<br>
<br>
이러한 접근 방식을 통해 코드의 가독성과 유지보수성을 크게 향상시킬 수 있다.<br>
<br><br><br>

## 주의 사항
확장 메서드 사용 시 주의해야할 몇 가지 사항들이 있다.<br>
<br>
- 확장 메서드는 기존 메서드보다 우선 순위가 낮다.<br>
즉, 같은 시그니처의 메서드가 타입 내에 존재한다면 확장 메서드 대신 타입 내의 메서드가 호출된다.<br>
<br>
- 확장 메서드는 타입의 내부 상태(`private` 필드나 `property`)에 직접 접근할 수 없다.<br>
따라서, 타입의 내부 구현을 변경할 수는 없으며, 공개된 `API` 를 통해서만 타입과 상호작용할 수 있다.<br>
<br>
- 명칭 공간(Namespace) 관리에 주의해야 한다.<br>
확장 메서드가 포함된 명칭 공간이 `using` 으로 포함되지 않으면, 해당 확장메서드는 '보이지' 않는다.<br>
<br><br><br>

## 결론
확장 메서드는 `C#` 에서 제공하는 강력하면서도 유연한 기능이다.<br>
<br>
이를 통해, 기존 코드에 영향을 주지 않고도 새로운 기능을 쉽게 추가할 수 있다.<br>
<br>
다만, 이 기능을 사용할 때는 타입의 설계 원칙과 캡슐화를 존중하는 방식으로 접근하는 것이 중요하다.<br>
<br>
확장 메서드를 현명하게 잘 활용하면, 코드의 가독성과 재사용성을 크게 향상시킬 수 있다.<br>
<br>
<br>
<br>
