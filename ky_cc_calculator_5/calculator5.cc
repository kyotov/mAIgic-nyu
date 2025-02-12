#include <ky/calculator5/calculator5.h>

namespace ky::calculator5 {

int add(int x, int y) {
  if (add_override) {
    return add_override(x, y);
  }
  return x + y;
}

} // namespace ky::calculator5