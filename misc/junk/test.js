function calculateAverage(arr) {
    if (arr.length === 0) return 0; // Handle empty array case

    let sum = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    let average = sum / arr.length;

    return average;
}

// Example usage
let numbers = [10, 20, 30, 40, 50];
let avg = calculateAverage(numbers);
console.log("Average:", avg);
