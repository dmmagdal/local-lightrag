# graphdb.py


from typing import List

import ladybug


class LadybugGraphDB:
	def __init__(self, db_path: str):
		self.db = ladybug.Database(db_path)
		self.conn = ladybug.Connection(self.db)


	def add_entity(self, ent_name: str, entity: str, ent_label: str = "UNK") -> None:
		self.conn.execute(
			"MERGE (e:Entity {id: $id, label: $l, desc: $d})",
			{
				"id": ent_name, 
				"l": ent_label, 
				"d": entity
			}
		)
	

	def add_triplet(self, source: str, target: str, relationship: str = "UNK", summary: str = "") -> None:
		self.conn.execute(
			"MATCH (a:Entity {id: $s}), (b:Entity {id: $t}) MERGE (a)-[:RELATES {relation: $r, desc: $d}]->(b)",
            {
				"s": source.lower(), 
				"t": target.lower(), 
				"r": relationship, 
				"d": summary
			}
		)


	def query(self, entity_id: str) -> List[str]:
		return self.conn.execute(
			"MATCH (a:Entity {id: $id})-[r:RELATES]->(b) RETURN a.id, r.relation, b.id",
			{
				"id": entity_id
			}
		)