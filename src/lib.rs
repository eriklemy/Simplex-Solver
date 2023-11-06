use ndarray::*;

/// Constraints you can add to your LP problem
///
/// Equal is x + y + z = N
/// LessThan is x + y + z <= N
/// GreaterThan is x + y + z >= N
#[derive(Clone, Debug)]
pub enum SimplexConstraint {
    EqualTo(Vec<f64>, f64),
    LessThan(Vec<f64>, f64),
    GreaterThan(Vec<f64>, f64),
}

impl SimplexConstraint {
    pub fn get_vector(&self) -> &Vec<f64> {
        match self {
            SimplexConstraint::EqualTo(a, _b) => a,
            SimplexConstraint::LessThan(a, _b) => a,
            SimplexConstraint::GreaterThan(a, _b) => a,
        }
    }

    pub fn get_const(&self) -> f64 {
        match self {
            SimplexConstraint::EqualTo(_a, b) => *b,
            SimplexConstraint::LessThan(_a, b) => *b,
            SimplexConstraint::GreaterThan(_a, b) => *b,
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum SimplexVar {
    Real,
    Slack(usize),
    NegativeSlack(usize),
    Artificial(usize),
}

impl SimplexVar {
    fn is_artificial(&self) -> bool {
        match self {
            SimplexVar::Artificial(_) => true,
            _ => false,
        }
    }

    fn is_slack(&self) -> bool {
        match self {
            SimplexVar::Slack(_) => true,
            _ => false,
        }
    }
}

#[derive(Debug, PartialEq)]
pub enum SimplexOutput {
    UniqueOptimum(f64),
    MultipleOptimum(f64),
    InfiniteSolution,
    NoSolution,
}

pub struct SimplexTable {
    objective: Vec<f64>,
    table: Array2<f64>,
    base: Vec<usize>,
    vars: Vec<SimplexVar>,
}

impl SimplexTable {
    fn get_entry_var(&self) -> Option<usize> {
        let mut entry_var = None;
        let mut max_entry = -1.0;
        for (i, z) in self.table.row(0).iter().enumerate() {
            if i == 0 || i == self.table.ncols() - 1 {
                continue;
            }
            if max_entry < *z {
                max_entry = *z;
                entry_var = Some(i);
            }
        }
        entry_var
    }

    fn get_exit_var(&self, entry_var: usize) -> Option<usize> {
        let mut exit_var = None;
        let mut min_entry = f64::MAX;
        let b = self.table.column(self.table.ncols() - 1);
        for (i, z) in self.table.column(entry_var).iter().enumerate() {
            if i == 0 {
                continue;
            }
            if *z <= 0.0 {
                continue;
            }
            if min_entry > b[i] / z {
                min_entry = b[i] / z;
                exit_var = Some(self.base[i - 1]);
            }
        }
        exit_var
    }

    fn step(&mut self, entry_var: usize, exit_var: usize) {
        let exit_row = self.base.iter().position(|x| *x == exit_var).unwrap() + 1;
        let pivot = self.table.row(exit_row)[entry_var];
        {
            let mut row = self.table.row_mut(exit_row);
            row /= pivot;
        }
        for i in 0..self.table.nrows() {
            if i == exit_row {
                continue;
            }
            let mut exit_row = self.table.row(exit_row).to_owned();
            let mut row = self.table.row_mut(i);
            let factor = row[entry_var] / -1.0;
            exit_row *= factor;
            row += &exit_row;
        }
        self.base = self
            .base
            .iter_mut()
            .map(|x| if *x == exit_var { entry_var } else { *x })
            .collect();
    }

    pub fn solve(&mut self) -> SimplexOutput {
        loop {
            if let Some(entry_var) = self.get_entry_var() {
                if let Some(exit_var) = self.get_exit_var(entry_var) {
                    self.step(entry_var, exit_var);
                } else {
                    return SimplexOutput::InfiniteSolution;
                }
            } else {
                panic!("Can't continue");
            }
            let mut optimum = true;
            let mut unique = true;
            for (i, &z) in self.table.row(0).iter().skip(1).enumerate() {
                optimum = optimum && z <= 0.0;
                if !self.base.contains(&i) && i <= self.objective.len() {
                    unique = unique && z - self.objective[i] < 0.0;
                }
            }
            if optimum {
                let optimum = self.table.row(0)[self.table.ncols() - 1];
                for (i, var) in self.base.iter().enumerate() {
                    if self.vars[*var - 1].is_artificial() {
                        if self.table.row(i + 1)[self.table.ncols() - 1] > 0.0 {
                            /* Artificial variable might have taken slack var value */
                            if self.vars[*var - 2].is_slack() {
                                if self.table.row(0)[*var - 1] == 0.0 {
                                    continue;
                                }
                            }
                            return SimplexOutput::NoSolution;
                        }
                    }
                }
                if unique {
                    return SimplexOutput::UniqueOptimum(optimum);
                } else {
                    return SimplexOutput::MultipleOptimum(optimum);
                }
            }
        }
    }

    pub fn get_var(&self, var: usize) -> Option<f64> {
        if var > self.objective.len() {
            return None;
        }
        for (i, v) in self.base.iter().enumerate() {
            if *v == var {
                return Some(self.table.row(i + 1)[self.table.ncols() - 1]);
            }
        }
        return Some(0.0);
    }
}

pub struct Simplex {
    objective: Vec<f64>,
}

impl Simplex {
    pub fn with(self, constraints: Vec<SimplexConstraint>) -> Result<SimplexTable, String> {
        let mut table = Vec::new();
        let mut vars = Vec::new();
        table.push(1.0);
        for var in self.objective.iter() {
            table.push(var * -1.0);
            vars.push(SimplexVar::Real);
        }
        for (i, constraint) in constraints.iter().enumerate() {
            match constraint {
                SimplexConstraint::LessThan(_, _) => {
                    table.push(0.0);
                    vars.push(SimplexVar::Slack(i));
                }
                SimplexConstraint::GreaterThan(_, _) => {
                    table.push(0.0);
                    vars.push(SimplexVar::NegativeSlack(i));
                }
                _ => {}
            }
            table.push(f64::MIN);
            vars.push(SimplexVar::Artificial(i));
        }
        table.push(0.0);

        for (i, constraint) in constraints.iter().enumerate() {
            table.push(0.0);
            for a in constraint.get_vector() {
                table.push(*a);
            }
            for var in vars.iter() {
                match var {
                    SimplexVar::Slack(j) => {
                        if *j == i {
                            table.push(1.0);
                        } else {
                            table.push(0.0);
                        }
                    }
                    SimplexVar::NegativeSlack(j) => {
                        if *j == i {
                            table.push(-1.0);
                        } else {
                            table.push(0.0);
                        }
                    }
                    SimplexVar::Artificial(j) => {
                        if *j == i {
                            table.push(1.0);
                        } else {
                            table.push(0.0);
                        }
                    }
                    _ => {}
                }
            }
            table.push(constraint.get_const());
        }
        let base: Vec<usize> = vars
            .iter()
            .enumerate()
            .filter_map(|(i, x)| if x.is_artificial() { Some(i + 1) } else { None })
            .collect();
        let table = Array2::from_shape_vec((base.len() + 1, vars.len() + 2), table);
        match table {
            Ok(table) => Ok(SimplexTable {
                objective: self.objective,
                table,
                base,
                vars,
            }),
            Err(_) => Err(String::from("Invalid matrix")),
        }
    }

    pub fn minimize(objective: &Vec<f64>) -> Self {
        Self {
            objective: objective.clone(),
        }
    }

    pub fn maximize(objective: &Vec<f64>) -> Self {
        let mut objective_max = objective.clone();
        for coeff in &mut objective_max {
            *coeff = -1.0;
        }
        Self {
            objective: objective_max,
        }
    }
}
