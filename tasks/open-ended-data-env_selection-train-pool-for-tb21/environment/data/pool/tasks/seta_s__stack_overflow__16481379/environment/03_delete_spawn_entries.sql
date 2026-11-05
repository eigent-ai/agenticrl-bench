DELETE s FROM spawn_entries s INNER JOIN npc_templates n ON s.npc_template_id = n.id_template WHERE n.type = 'monster';
