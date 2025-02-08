const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter the coefficient of x^3: ', (a) => {
  rl.question('Enter the coefficient of x^2: ', (b) => {
    rl.question('Enter the coefficient of x: ', (c) => {
      rl.question('Enter the constant term: ', (d) => {
        try {
          const roots = solveCubicEquation(parseFloat(a), parseFloat(b), parseFloat(c), parseFloat(d));
          console.log('Roots of the equation are:', roots);
        } catch (error) {
          console.error('Invalid input. Please enter numerical values.');
        }
        rl.close();
      });
    });
  });
});

function solveCubicEquation(a, b, c, d) {
  if (a === 0) {
    // Handle the case when the equation is not cubic
    throw new Error('The coefficient of x^3 cannot be zero.');
  }

  // Implement the cubic equation solving algorithm here
  // ...
}