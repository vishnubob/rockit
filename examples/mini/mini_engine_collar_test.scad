

union() {
	union() {
		union() {
			difference() {
				cylinder($fn = 200, h = 65.7859644756, r = 13.9499931420);
				cylinder($fn = 200, h = 65.7859644756, r = 12.6999931420);
			}
			union() {
				translate(v = [0, 0, 56.8959692762]) {
					difference() {
						cylinder(r1 = 13.9499931420, r2 = 12.5094932449, $fn = 200, h = 8.8899951994);
						cylinder(r1 = 12.6999931420, r2 = 11.2594932449, $fn = 200, h = 8.8899951994);
					}
				}
				difference() {
					translate(v = [0, 0, 65.7859644756]) {
						difference() {
							cylinder($fn = 200, h = 8.8899951994, r = 12.5094932449);
							cylinder($fn = 200, h = 8.8899951994, r = 11.2594932449);
						}
					}
					translate(v = [0, 0, 73.6759596750]) {
						difference() {
							cylinder(r1 = 13.0094932449, r2 = 13.0094932449, $fn = 200, h = 2);
							cylinder(r1 = 12.5094932449, r2 = 10.7594932449, $fn = 200, h = 2);
						}
					}
				}
			}
		}
		union() {
			translate(v = [0, 0, 56.8959692762]) {
				difference() {
					cylinder(r1 = 13.9499931420, r2 = 12.5094932449, $fn = 200, h = 8.8899951994);
					cylinder(r1 = 12.6999931420, r2 = 11.2594932449, $fn = 200, h = 8.8899951994);
				}
			}
			difference() {
				translate(v = [0, 0, 65.7859644756]) {
					difference() {
						cylinder($fn = 200, h = 8.8899951994, r = 12.5094932449);
						cylinder($fn = 200, h = 8.8899951994, r = 11.2594932449);
					}
				}
				translate(v = [0, 0, 73.6759596750]) {
					difference() {
						cylinder(r1 = 13.0094932449, r2 = 13.0094932449, $fn = 200, h = 2);
						cylinder(r1 = 12.5094932449, r2 = 10.7594932449, $fn = 200, h = 2);
					}
				}
			}
		}
	}
	translate(v = [30.6899849124, 0, 0]) {
		union() {
			union() {
				difference() {
					cylinder($fn = 200, h = 65.7859644756, r = 13.9499931420);
					cylinder($fn = 200, h = 65.7859644756, r = 12.6999931420);
				}
				union() {
					translate(v = [0, 0, 56.8959692762]) {
						difference() {
							cylinder(r1 = 13.9499931420, r2 = 12.5094932449, $fn = 200, h = 8.8899951994);
							cylinder(r1 = 12.6999931420, r2 = 11.2594932449, $fn = 200, h = 8.8899951994);
						}
					}
					difference() {
						translate(v = [0, 0, 65.7859644756]) {
							difference() {
								cylinder($fn = 200, h = 8.8899951994, r = 12.5094932449);
								cylinder($fn = 200, h = 8.8899951994, r = 11.2594932449);
							}
						}
						translate(v = [0, 0, 73.6759596750]) {
							difference() {
								cylinder(r1 = 13.0094932449, r2 = 13.0094932449, $fn = 200, h = 2);
								cylinder(r1 = 12.5094932449, r2 = 10.7594932449, $fn = 200, h = 2);
							}
						}
					}
				}
			}
			union() {
				translate(v = [0, 0, 56.8959692762]) {
					difference() {
						cylinder(r1 = 13.9499931420, r2 = 12.5094932449, $fn = 200, h = 8.8899951994);
						cylinder(r1 = 12.6999931420, r2 = 11.2594932449, $fn = 200, h = 8.8899951994);
					}
				}
				difference() {
					translate(v = [0, 0, 65.7859644756]) {
						difference() {
							cylinder($fn = 200, h = 8.8899951994, r = 12.5094932449);
							cylinder($fn = 200, h = 8.8899951994, r = 11.2594932449);
						}
					}
					translate(v = [0, 0, 73.6759596750]) {
						difference() {
							cylinder(r1 = 13.0094932449, r2 = 13.0094932449, $fn = 200, h = 2);
							cylinder(r1 = 12.5094932449, r2 = 10.7594932449, $fn = 200, h = 2);
						}
					}
				}
			}
		}
	}
}