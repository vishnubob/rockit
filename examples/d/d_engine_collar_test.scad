

union() {
	union() {
		union() {
			difference() {
				cylinder($fn = 200, h = 89.0269519254, r = 19.6649900559);
				cylinder($fn = 200, h = 89.0269519254, r = 18.4149900559);
			}
			union() {
				translate(v = [0, 0, 80.1369567260]) {
					difference() {
						cylinder(r1 = 19.6649900559, r2 = 18.1387652051, $fn = 200, h = 8.8899951994);
						cylinder(r1 = 18.4149900559, r2 = 16.8887652051, $fn = 200, h = 8.8899951994);
					}
				}
				difference() {
					translate(v = [0, 0, 89.0269519254]) {
						difference() {
							cylinder($fn = 200, h = 8.8899951994, r = 18.1387652051);
							cylinder($fn = 200, h = 8.8899951994, r = 16.8887652051);
						}
					}
					translate(v = [0, 0, 96.9169471248]) {
						difference() {
							cylinder(r1 = 18.6387652051, r2 = 18.6387652051, $fn = 200, h = 2);
							cylinder(r1 = 18.1387652051, r2 = 16.3887652051, $fn = 200, h = 2);
						}
					}
				}
			}
		}
		union() {
			translate(v = [0, 0, 80.1369567260]) {
				difference() {
					cylinder(r1 = 19.6649900559, r2 = 18.1387652051, $fn = 200, h = 8.8899951994);
					cylinder(r1 = 18.4149900559, r2 = 16.8887652051, $fn = 200, h = 8.8899951994);
				}
			}
			difference() {
				translate(v = [0, 0, 89.0269519254]) {
					difference() {
						cylinder($fn = 200, h = 8.8899951994, r = 18.1387652051);
						cylinder($fn = 200, h = 8.8899951994, r = 16.8887652051);
					}
				}
				translate(v = [0, 0, 96.9169471248]) {
					difference() {
						cylinder(r1 = 18.6387652051, r2 = 18.6387652051, $fn = 200, h = 2);
						cylinder(r1 = 18.1387652051, r2 = 16.3887652051, $fn = 200, h = 2);
					}
				}
			}
		}
	}
	translate(v = [43.2629781230, 0, 0]) {
		union() {
			union() {
				difference() {
					cylinder($fn = 200, h = 89.0269519254, r = 19.6649900559);
					cylinder($fn = 200, h = 89.0269519254, r = 18.4149900559);
				}
				union() {
					translate(v = [0, 0, 80.1369567260]) {
						difference() {
							cylinder(r1 = 19.6649900559, r2 = 18.1387652051, $fn = 200, h = 8.8899951994);
							cylinder(r1 = 18.4149900559, r2 = 16.8887652051, $fn = 200, h = 8.8899951994);
						}
					}
					difference() {
						translate(v = [0, 0, 89.0269519254]) {
							difference() {
								cylinder($fn = 200, h = 8.8899951994, r = 18.1387652051);
								cylinder($fn = 200, h = 8.8899951994, r = 16.8887652051);
							}
						}
						translate(v = [0, 0, 96.9169471248]) {
							difference() {
								cylinder(r1 = 18.6387652051, r2 = 18.6387652051, $fn = 200, h = 2);
								cylinder(r1 = 18.1387652051, r2 = 16.3887652051, $fn = 200, h = 2);
							}
						}
					}
				}
			}
			union() {
				translate(v = [0, 0, 80.1369567260]) {
					difference() {
						cylinder(r1 = 19.6649900559, r2 = 18.1387652051, $fn = 200, h = 8.8899951994);
						cylinder(r1 = 18.4149900559, r2 = 16.8887652051, $fn = 200, h = 8.8899951994);
					}
				}
				difference() {
					translate(v = [0, 0, 89.0269519254]) {
						difference() {
							cylinder($fn = 200, h = 8.8899951994, r = 18.1387652051);
							cylinder($fn = 200, h = 8.8899951994, r = 16.8887652051);
						}
					}
					translate(v = [0, 0, 96.9169471248]) {
						difference() {
							cylinder(r1 = 18.6387652051, r2 = 18.6387652051, $fn = 200, h = 2);
							cylinder(r1 = 18.1387652051, r2 = 16.3887652051, $fn = 200, h = 2);
						}
					}
				}
			}
		}
	}
}