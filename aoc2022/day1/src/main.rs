use utils;

fn main() {
    println!("Part 1: {}", part1("2022/day1/input"));
    println!("Part 2: {}", part2("2022/day1/input"));
}

fn parse_input(path: &str) -> Vec<Vec<usize>> {
    use std::fs::read_to_string;
    read_to_string(path)
        .expect("Input file should be read")
        .trim()
        .split("\n\n")
        .map(|x| subparse(x))
        .collect()
}

fn subparse(input: &str) -> Vec<usize> {
    input
        .split("\n")
        .map(|x| x.parse::<usize>().expect("Parsed string should be an int"))
        .collect()
}

fn part1(path: &str) -> usize {
    parse_input(path)
        .iter()
        .map(|v| v.iter().sum::<usize>())
        .max()
        .unwrap()
}

fn part2(path: &str) -> usize {
    use std::collections::BinaryHeap;
    let mut top_three = Vec::new();
    let mut calories: BinaryHeap<usize> = parse_input(path)
        .iter()
        .map(|v| v.iter().sum::<usize>())
        .collect();
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

    #[test]
    fn example_parse() {
        assert_eq!(
            parse_input("example"),
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
        assert_eq!(part1("example"), 24000);
    }

    #[test]
    fn example_p2() {
        assert_eq!(part2("example"), 45000);
    }
}
