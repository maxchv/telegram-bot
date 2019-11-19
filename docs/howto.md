
# Создание телеграм бота. Пошаговая инструкция

## Язык программирования Python. Быстрый старт

### Типы данных

Целые (`int`)

```python
>>> 10
10
>>> type(10)
<type 'int'>
```

С плавающей точкой (`float`)

```python
>>> 10.0
10.0
>>> type(10.0)
<type 'float'>
```

Строки (`str`)

```python
>>> 'Hello World'
"Hello World"
>>> type("Hello World")
<type 'str'>
```

Логический (`bool`)

```python
>>> True
True
>>> type(True)
<type 'bool'>
>>> False
False
>>> type(False)
<type 'bool'>
```

Списки (`list`)

```python
>>> [10, 'Hello World']
[10, 'Hello World']
>>> type([10, 'Hello World'])
<type 'list'>
```

<!-- Кортежи (`tuple`)

```python
>>> 10, 'Hello World'
(10, 'Hello World')
>>> type((10, 'Hello World'))
<type 'typle'>
``` -->

Словари (`dict`)

```python
>>> {0: 'first', 1: 'second' }
{0: 'first', 1: 'second'}
>>> type({0: 'first', 1: 'second'})
<type 'dict'>
```

### Переменные

Переменная - именованая ячейка данных в памяти компьютера.

```python
>>> a = 10
>>> print(a)
10
>>> a = 'I Love Python'
>>> print(a)
I Love Python
```

Значение переменных (и тип данных) можно менять

### Логический тип данных

Что есть правда?

```python
>>> True
True
>>> bool(1)
True
>>> bool(0)
False
>>> bool('')
False
>>> bool('0')
True
>>> bool([])
False
>>> bool([0])
True
>>> bool({})
False
>>> bool({0: 'zero'})
True
```

Условные операторы: `>, <, >=, <=, ==, !=`

```python
>>> 10 > 5
True
>>> a = 10
>>> b = 20
>>> a > b
False
```

Операторы: `and, or, not`

```python
>>> True and True
True
>>> True and False
False
>>> False and False
False
>>> True or True
True
>>> True or False
True
>>> False or False
False
>>> not True
False
>>> not False
True
```

### Условия

Условное выполнение:

```python
>>> if hp > 0:
...     print('You are live')
... else:
...     print('You are die')
You are live
```

Множественные условия:

```python
>>> x = 42
>>> if x % 5 == 0:
...     print("fizz")
... elif x % 3 == 0:
...     print("buzz")
... else:
...     pass # необязательная ветка
buzz
```

### Циклы

### Функции

### Декораторы

## Создание бота

