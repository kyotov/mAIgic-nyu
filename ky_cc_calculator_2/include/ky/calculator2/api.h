#pragma once

namespace ky::calculator2 {

class Calculator2 {
public:
  virtual ~Calculator2();

  virtual float binary_operation(float x, float y) const = 0;

  // factory method
  static const Calculator2 &get_instance();
};

} // namespace ky::calculator2
