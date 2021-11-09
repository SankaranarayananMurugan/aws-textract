import json
from functools import reduce
from analysedocument.enums import BlockType, RelationshipType, EntityType

class TextractAnalysis():
    def initialise_block_buckets(self):
        return {
            EntityType.KEY: {},
            EntityType.VALUE: {},
            BlockType.WORD: {},
            BlockType.LINE: []
        }

    def get_block_type(self, block):
        block_type_value = block.get('BlockType', '')
        return BlockType(block_type_value)

    def get_entity_type(self, block):
        entity_type_value = block.get('EntityTypes', [-1])[0]
        return EntityType(entity_type_value)

    def get_relationship_type(self, relationship):
        relationship_type_value = relationship.get('Type', '')
        return RelationshipType(relationship_type_value)

    def get_block_buckets(self, document_dict_list):
        block_buckets = self.initialise_block_buckets()

        for document_dict in document_dict_list:
            for block in document_dict.get('Blocks', []):
                block_type = self.get_block_type(block)
                if block_type == BlockType.KEY_VALUE_SET:
                    entity_type = self.get_entity_type(block)
                    if entity_type == EntityType.KEY or entity_type == EntityType.VALUE:
                        key_value_dict = block_buckets.get(entity_type)
                        key_value_dict[block.get('Id')] = block
                elif block_type == BlockType.WORD:
                    word_dict = block_buckets.get(block_type)
                    word_dict[block.get('Id')] = block
                elif block_type == BlockType.LINE:
                    line_list = block_buckets.get(block_type)
                    line_list.append(block)
        
        return block_buckets

    def extract_key_value_ref(self, key_blocks):
        key_value_ref_list = []
        for key_id in key_blocks:
            key_block = key_blocks.get(key_id)

            key, value = [], []
            for relationship in key_block.get('Relationships', []):
                relationship_type = self.get_relationship_type(relationship)
                if relationship_type == RelationshipType.CHILD:
                    key = relationship.get('Ids', [])
                elif relationship_type == RelationshipType.VALUE:
                    value = relationship.get('Ids', [])

            key_value_ref_list.append({
                'key': key,
                'value': value
            })

        return key_value_ref_list
                    
    def resolve_value_ref(self, value_blocks, key_value_ref_list):
        for key_value_ref in key_value_ref_list:            
            value_ref = key_value_ref.get('value', [-1])            
            value_block = value_blocks.get(value_ref[0])
            
            if value_block is not None:
                for relationship in value_block.get('Relationships', {}):
                    relationship_type = self.get_relationship_type(relationship)
                    if relationship_type == RelationshipType.CHILD:
                        key_value_ref['value'] = relationship.get('Ids', [])

    def resolve_key_value(self, word_blocks, key_value_ref_list):
        key_value_dict = {}
        for key_value_ref in key_value_ref_list:
            key_ref = key_value_ref.get('key')
            key = self.resolve_word(word_blocks, key_ref)

            value_ref = key_value_ref.get('value')
            value = self.resolve_word(word_blocks, value_ref)

            key_value_dict[key] = value

        return key_value_dict

    # Concatenate text from related word blocks
    def resolve_word(self, word_blocks, ref):
        def concat_word_block_text(result, word_id):
            word_block_text = word_blocks.get(word_id, {}).get('Text', '')
            return result + ' ' + word_block_text
        
        resolved_word = reduce(concat_word_block_text, ref, '').strip()
        
        # Remove identified words to find orphan word blocks
        for index in ref:
            word_blocks.pop(index, None)

        return resolved_word

    def get_line_children(self, line_block):
        for relationship in line_block.get('Relationships', []):
            relationship_type = self.get_relationship_type(relationship)
            if relationship_type == RelationshipType.CHILD:
                return relationship.get('Ids', [])

    def find_orphan_lines(self, word_blocks, line_blocks):
        orphan_line_list = []
        for line_block in line_blocks:
            line_children = self.get_line_children(line_block)
            for line_child in line_children:
                if line_child in word_blocks.keys():
                    orphan_value = line_block.get('Text')
                    if len(orphan_value) > 0:
                        orphan_line_list.append(orphan_value)
                    break
        return orphan_line_list

    def extract_key_value(self, textract_document):
        block_buckets = self.get_block_buckets(textract_document)
        
        # Extracts key and value refs [Value refs are not real]
        key_blocks = block_buckets.get(EntityType.KEY)
        key_value_ref_list = self.extract_key_value_ref(key_blocks)

        # Resolves value refs
        value_blocks = block_buckets.get(EntityType.VALUE)
        self.resolve_value_ref(value_blocks, key_value_ref_list)        

        # Resolves actual key and value
        word_blocks = block_buckets.get(BlockType.WORD)
        key_value_dict = self.resolve_key_value(word_blocks, key_value_ref_list)

        # Find orphan lines without keys
        line_blocks = block_buckets.get(BlockType.LINE)
        orphan_line_list = self.find_orphan_lines(word_blocks, line_blocks)
        key_value_dict['Others'] = orphan_line_list

        return key_value_dict

    def read_analysed_document(self, document_name):
        analysed_file = open('analyse_results/' + document_name + '.json', 'r')
        analysed_result = analysed_file.read()
        analysed_file.close()
        return json.loads(analysed_result)

    def write_analysed_document(self, document_name, document_content):
        analysed_file = open('analyse_results/' + document_name + '.json', 'w')
        analysed_file.write(json.dumps(document_content))
        analysed_file.close()
