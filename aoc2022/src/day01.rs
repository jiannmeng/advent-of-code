use super::utils;

const INPUT: &str = "inputs/01/input";

pub fn main() {
    printday!(1, part1(INPUT), part2(INPUT));
}

fn parse_input(input: &str) -> Vec<Vec<usize>> {
    utils::get_input(input)
        .split("\n\n")
        .map(subparse)
        .collect()
}

fn subparse(input: &str) -> Vec<usize> {
    input
        .split('\n')
        .map(|x| x.parse::<usize>().expect("Parsed string should be an int"))
        .collect()
}

fn part1(input: &str) -> usize {
    parse_input(input)
        .iter()
        .map(|v| v.iter().sum::<usize>())
        .max()
        .unwrap()
}

fn part2(input: &str) -> usize {
    // BinaryHeap sorts the entries, and .pop() gives the largest value in the heap.
    use std::collections::BinaryHeap;
    let mut calories: BinaryHeap<usize> = parse_input(input)
        .iter()
        .map(|v| v.iter().sum::<usize>())
        .collect();

    let mut top_three = Vec::new();
    for _ in 0..3 {
        if let Some(n) = calories.pop() {
            top_three.push(n);
        }
    }
    top_three.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "inputs/01/example";

    #[test]
    fn example_parse() {
        assert_eq!(
            parse_input(EXAMPLE),
            vec![
                vec![1000, 2000, 3000],
                vec![4000],
                vec![5000, 6000],
                vec![7000, 8000, 9000],
                vec![10000],
            ]
        )
    }

    #[test]
    fn example_p1() {
        assert_eq!(part1(EXAMPLE), 24000);
    }

    #[test]
    fn example_p2() {
        assert_eq!(part2(EXAMPLE), 45000);
    }

    #[test]
    fn input_p1() {
        assert_eq!(part1(INPUT), 69528);
    }

    #[test]
    fn input_p2() {
        assert_eq!(part2(INPUT), 206152);
    }
}
