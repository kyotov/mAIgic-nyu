namespace ky {

class Calculator {
public:
  Calculator(int seed);

  int add(int a, int b);

private:
  int seed;
};

} // namespace ky
