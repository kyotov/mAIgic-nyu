#include <calculator.h>
#include <iostream>

int main() {
  ky::Calculator calc(42);
  std::cout << "Hello, World! " << calc.add(2, 2) << std::endl;
  return 0;
}
