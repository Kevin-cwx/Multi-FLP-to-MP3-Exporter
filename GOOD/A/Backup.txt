# Backup
def filter_tree(self, event):
     search_term = self.search_entry.get().lower()

      """Filter tree items based on search term"""
       # Check if placeholder is active
       if self.placeholder_active:
            search_term = ""
        else:
            search_term = self.search_entry.get().lower()

        # If search term is empty, restore original tree state
        if not search_term:
            self.restore_tree_state()
            return

        # Store current tree state if not already stored
        if not self.original_tree_state:
            self.store_tree_state()

        # First, hide all items
        for item in self.tree.get_children():
            self.hide_item_and_children(item)

        # Show items that match the search term
        for item_id, item_text in self.all_items.items():
            if search_term in item_text.lower():
                self.show_item_and_parents(item_id)
                # If it's a folder, look for matches in children
                if self.tree.get_children(item_id):
                    for child in self.tree.get_children(item_id):
                        child_text = self.tree.item(child)['text']
                        if search_term in child_text.lower():
                            self.tree.reattach(child, item_id, 'end')
                            self.tree.item(item_id, open=True)
            search_term = self.search_entry.get().lower()

            # If search term is empty, restore original tree state
            if not search_term:
                self.restore_tree_state()
                return

            # Store current tree state if not already stored
            if not self.original_tree_state:
                self.store_tree_state()

            # First, hide all items
            for item in self.tree.get_children():
                self.tree.item(item, open=False)
                self.hide_item_and_children(item)

        # Show items that match the search term
            for item_id, item_text in self.all_items.items():
                if search_term in item_text.lower():
                    self.show_item_and_parents(item_id)
                    # If it's a folder, look for matches in children
                    if self.tree.get_children(item_id):
                        for child in self.tree.get_children(item_id):
                            child_text = self.tree.item(child)['text']
                            if search_term in child_text.lower():
                                self.tree.reattach(child, item_id, 'end')
                                self.tree.item(item_id, open=True)
