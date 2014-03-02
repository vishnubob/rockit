

union() {
	union() {
		difference() {
			cylinder($fn = 200, h = 93.2179496623, r = 16.3629918390);
			cylinder($fn = 200, h = 93.2179496623, r = 15.1129918390);
		}
		union() {
			translate(v = [0, 0, 84.3279544629]) {
				difference() {
					cylinder(r1 = 16.3629918390, r2 = 14.8862969614, $fn = 200, h = 8.8899951994);
					cylinder(r1 = 15.1129918390, r2 = 13.6362969614, $fn = 200, h = 8.8899951994);
				}
			}
			difference() {
				translate(v = [0, 0, 93.2179496623]) {
					difference() {
						cylinder($fn = 200, h = 8.8899951994, r = 14.8862969614);
						cylinder($fn = 200, h = 8.8899951994, r = 13.6362969614);
					}
				}
				translate(v = [0, 0, 101.1079448617]) {
					difference() {
						cylinder(r1 = 15.3862969614, r2 = 15.3862969614, $fn = 200, h = 2);
						cylinder(r1 = 14.8862969614, r2 = 13.1362969614, $fn = 200, h = 2);
					}
				}
			}
		}
	}
	union() {
		difference() {
			cylinder(r1 = 16.3629918390, r2 = 10.7140348894, $fn = 200, h = 8.8899951994);
			cylinder(r1 = 15.1129918390, r2 = 9.4640348894, $fn = 200, h = 8.8899951994);
		}
		translate(v = [0, 0, 8.8899951994]) {
			difference() {
				cylinder($fn = 200, h = 84.3279544629, r = 10.7140348894);
				cylinder($fn = 200, h = 84.3279544629, r = 9.4640348894);
			}
		}
		translate(v = [0, 0, 84.3279544629]) {
			difference() {
				cylinder(r1 = 16.3629918390, r2 = 16.3629918390, $fn = 200, h = 8.8899951994);
				cylinder(r1 = 10.7140348894, r2 = 8.1138845074, $fn = 200, h = 8.8899951994);
			}
		}
	}
	rotate(a = [0, 0, 0.0000000000]) {
		polyhedron(points = [[16.3624918390, 0.6250000000, 0], [16.3624918390, -0.6250000000, 0], [57.2704714364, 0.6250000000, 0], [57.2704714364, -0.6250000000, 0], [57.2704714364, 0.6250000000, 27.9653848987], [57.2704714364, -0.6250000000, 27.9653848987], [16.3624918390, 0.6250000000, 74.5743597298], [16.3624918390, -0.6250000000, 74.5743597298]], triangles = [[0, 1, 2], [1, 3, 2], [2, 3, 4], [3, 5, 4], [4, 5, 6], [5, 7, 6], [6, 7, 0], [7, 1, 0], [0, 2, 6], [2, 4, 6], [1, 7, 3], [3, 7, 5]]);
	}
	rotate(a = [0, 0, 90.0000000000]) {
		polyhedron(points = [[16.3624918390, 0.6250000000, 0], [16.3624918390, -0.6250000000, 0], [57.2704714364, 0.6250000000, 0], [57.2704714364, -0.6250000000, 0], [57.2704714364, 0.6250000000, 27.9653848987], [57.2704714364, -0.6250000000, 27.9653848987], [16.3624918390, 0.6250000000, 74.5743597298], [16.3624918390, -0.6250000000, 74.5743597298]], triangles = [[0, 1, 2], [1, 3, 2], [2, 3, 4], [3, 5, 4], [4, 5, 6], [5, 7, 6], [6, 7, 0], [7, 1, 0], [0, 2, 6], [2, 4, 6], [1, 7, 3], [3, 7, 5]]);
	}
	rotate(a = [0, 0, 180.0000000000]) {
		polyhedron(points = [[16.3624918390, 0.6250000000, 0], [16.3624918390, -0.6250000000, 0], [57.2704714364, 0.6250000000, 0], [57.2704714364, -0.6250000000, 0], [57.2704714364, 0.6250000000, 27.9653848987], [57.2704714364, -0.6250000000, 27.9653848987], [16.3624918390, 0.6250000000, 74.5743597298], [16.3624918390, -0.6250000000, 74.5743597298]], triangles = [[0, 1, 2], [1, 3, 2], [2, 3, 4], [3, 5, 4], [4, 5, 6], [5, 7, 6], [6, 7, 0], [7, 1, 0], [0, 2, 6], [2, 4, 6], [1, 7, 3], [3, 7, 5]]);
	}
	rotate(a = [0, 0, 270.0000000000]) {
		polyhedron(points = [[16.3624918390, 0.6250000000, 0], [16.3624918390, -0.6250000000, 0], [57.2704714364, 0.6250000000, 0], [57.2704714364, -0.6250000000, 0], [57.2704714364, 0.6250000000, 27.9653848987], [57.2704714364, -0.6250000000, 27.9653848987], [16.3624918390, 0.6250000000, 74.5743597298], [16.3624918390, -0.6250000000, 74.5743597298]], triangles = [[0, 1, 2], [1, 3, 2], [2, 3, 4], [3, 5, 4], [4, 5, 6], [5, 7, 6], [6, 7, 0], [7, 1, 0], [0, 2, 6], [2, 4, 6], [1, 7, 3], [3, 7, 5]]);
	}
	rotate(a = [0, 0, 45.0000000000]) {
		translate(v = [18.8236155102, 0, 0]) {
			difference() {
				cylinder($fn = 200, h = 50.7999725680, r = 3.7106236713);
				cylinder($fn = 200, h = 50.7999725680, r = 2.4606236713);
			}
		}
	}
}