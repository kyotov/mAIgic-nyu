#include "calculator.h"

namespace ky {

Calculator::Calculator(int seed) : seed(seed) {}

int Calculator::add(int a, int b) { return a + b + seed; }

} // namespace ky