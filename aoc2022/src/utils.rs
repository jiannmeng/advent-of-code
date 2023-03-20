#![macro_use]

macro_rules! printday {
    ($day:expr, $part1:expr, $part2:expr) => {
        let start1 = std::time::Instant::now();
        let part1 = $part1;
        let duration1 = start1.elapsed().as_secs_f32();

        let start2 = std::time::Instant::now();
        let part2 = $part2;
        let duration2 = start2.elapsed().as_secs_f32();

        println!("----------------------");
        println!("Day {}:", $day);
        println!("  Part 1: {part1} | took {duration1}ms");
        println!("  Part 2: {part2} | took {duration2}ms");
    };
}

pub fn get_input(path: &str) -> String {
    use std::fs::read_to_string;
    read_to_string(path)
        .expect("Input file should be read")
        .trim()
        .to_string()
}
