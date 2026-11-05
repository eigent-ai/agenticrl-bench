SELECT ELT(FIELD(CEILING(RAND()*3), 1, 2, 3), 'Control', 'Treatment_A', 'Treatment_B') AS test_group;
