#include <calculator.h>
#include <nanobind/nanobind.h>

namespace nb = nanobind;

NB_MODULE(_calculator, m) {
  nb::class_<ky::Calculator>(m, "KyCalculator")
      .def(nb::init<int>())
      .def("add", &ky::Calculator::add);
}