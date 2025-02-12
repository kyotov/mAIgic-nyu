#include <calculator.h>
#include <iostream>
#include <ky/calculator2/api.h>
#include <ky/calculator2seed/calculator2seed.h>
#include <ky/calculator3/calculator3.h>
#include <ky/calculator4/calculator4.h>
#include <ky/calculator5/calculator5.h>

namespace ky::calculator5 {
int add_override(int x, int y) { return x * 1000 + y * 1000000; }
} // namespace ky::calculator5

int main() {
  ky::Calculator calc(42);
  std::cout << "Hello, World! #1 " << calc.add(2, 2) << std::endl;

  register_calculator2seed();

  auto &calc2 = ky::calculator2::Calculator2::get_instance();
  std::cout << "Hello, World! #2 " << calc2.binary_operation(2, 2) << std::endl;

  auto calc3 = ky::calculator3::Calculator3(10);
  std::cout << "Hello, World! #3a " << calc3.add(2, 2) << std::endl;
  std::cout << "Hello, World! #3a " << calc3.mul(2, 2) << std::endl;

  std::cout << "Hello, World! #4 " << ky::calculator4::add(2, 2) << std::endl;

  std::cout << "Hello, World! #5 " << ky::calculator5::add(2, 2) << std::endl;

  return 0;
}
