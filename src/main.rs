use regex::Regex;
use simplex_solver::*;
use std::io;
use std::io::Write;

// minimize: C: -3.0x1 + 1.0x2 -2.0x3
// s.a:
//     2.0x1 -2.0x2 + 3.0x3 <= 5.0
//     1.0x1 + 1.0x2 -1.0x3 <= 3.0
//     1.0x1 -1.0x2 + 1.0x3 <= 2.,
fn main() {
    let (function, program, vector) = get_user_input();
    println!("{:?}", vector);
    println!("Subjecto To (s.a): ");
    show_constraints(&vector);
    match program {
        Ok(mut simplex) => {
            println!("--------------------------------------------------------");
            println!("Solution: ");
            match simplex.solve() {
                SimplexOutput::UniqueOptimum(x) => println!("\t{}: {}", function, x),
                SimplexOutput::MultipleOptimum(x) => println!("\t{}: {}", function, x),
                _ => eprintln!("No solution or unbounded"),
            }
            println!("\tx1: {:?}", simplex.get_var(1));
            println!("\tx2: {:?}", simplex.get_var(2));
            println!("\tx3: {:?}", simplex.get_var(3));
        }
        Err(err) => {
            eprintln!("ERROR: {}", err);
        }
    }
}

fn get_user_input() -> (String, Result<SimplexTable, String>, Vec<SimplexConstraint>) {
    let (function, program);
    let mut vector = Vec::new();

    'exit: loop {
        print!("Desejar maximizar ou minimizar (Max/Min): ");
        let objective = get_str_input();

        print!("Digite a Função Objetivo: ");
        let object_func = get_str_input();
        let re = Regex::new(r"(-?\d+(?:\.\d+)?)\w").unwrap();

        let numbers: Vec<f64> = re
            .captures_iter(&object_func)
            .map(|capture| capture[1].parse().unwrap())
            .collect();
        println!("{:?}", numbers);
        println!("Digite as restrições: ");
        loop {
            let constraint = input_constraint();
            vector.push(constraint);

            println!("Digite a restrição: (Digite 's' para continuar ou qualquer outra coisa para encerrar):");
            let input = get_str_input();
            if input.trim() != "s" {
                break;
            }
        }

        let vector_clone = vector.clone(); // clone the vector before passing it to the `with()` function
        (function, program) = match objective[0..3].to_uppercase().as_str() {
            "MAX" => (
                "Z".to_string(),
                Simplex::maximize(&numbers).with(vector_clone),
            ),
            "MIN" => (
                "C".to_string(),
                Simplex::minimize(&numbers).with(vector_clone),
            ),
            _ => ("ERRO".to_string(), Err("Invalid objective".to_string())),
        };
        println!("--------------------------------------------------------");
        println!(
            "Objective Function:\n\t{function}: {}*x1 + ({}*x2) + ({}*x3)",
            numbers[0], numbers[1], numbers[2]
        );
        break 'exit;
    }

    (function, program, vector)
}

fn get_str_input() -> String {
    let mut input = String::new();
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().to_string()
}

fn show_constraints(constraints: &Vec<SimplexConstraint>) {
    for (_, constraint) in constraints.iter().enumerate() {
        let constraint_string = constraint_to_string(constraint);
        println!("\t{}", constraint_string);
    }
}

fn constraint_to_string(constraint: &SimplexConstraint) -> String {
    let sign = match constraint {
        SimplexConstraint::LessThan(_, _) => "<=",
        SimplexConstraint::GreaterThan(_, _) => ">=",
        SimplexConstraint::EqualTo(_, _) => "=",
    };

    let mut constraint_string = String::new();
    for (i, &coeff) in constraint.get_vector().iter().enumerate() {
        if i > 0 {
            if coeff >= 0.0 {
                constraint_string.push_str(" + ");
            } else {
                constraint_string.push_str(" - ");
            }
        }
        let variable = format!("x{}", i + 1);
        constraint_string.push_str(&format!("{:.1}*{}", coeff.abs(), variable));
    }

    constraint_string.push_str(&format!(" {} {:.1}", sign, constraint.get_const()));

    format!("\t{}", constraint_string)
}

fn input_constraint() -> SimplexConstraint {
    println!("Insira os coeficientes da restrição (separados por espaços):");
    let coefficients_input = get_str_input();

    let coefficients: Vec<f64> = coefficients_input
        .split_whitespace()
        .map(|coeff_str| coeff_str.parse().unwrap())
        .collect();

    println!("Insira o operador da restrição (<=, >=, =):");
    let operator = get_str_input();

    println!("Insira o valor da constante da restrição:");
    let constant_input = get_str_input();
    let constant = constant_input.parse::<f64>().unwrap();

    match operator.trim() {
        "<=" => SimplexConstraint::LessThan(coefficients, constant),
        ">=" => SimplexConstraint::GreaterThan(coefficients, constant),
        "=" => SimplexConstraint::EqualTo(coefficients, constant),
        _ => panic!("Operador inválido: {}", operator),
    }
}
