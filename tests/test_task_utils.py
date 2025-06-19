import unittest
import os
import csv
from utils.task_utils import load_tasks, save_result, calculate_summary

class TestTaskUtils(unittest.TestCase):

    def test_load_tasks_default(self):
        tasks = load_tasks("non_existent_file.json")
        self.assertIsInstance(tasks, list)
        self.assertTrue(len(tasks) > 0)

    def test_calculate_summary(self):
        results = [
            {"task": "A", "time_taken": 1.0, "success": True, "start_time": 0, "end_time": 1},
            {"task": "B", "time_taken": 2.0, "success": False, "start_time": 0, "end_time": 2},
            {"task": "C", "time_taken": 3.0, "success": True, "start_time": 0, "end_time": 3},
        ]
        summary = calculate_summary(results)
        self.assertEqual(summary['total'], 3)
        self.assertEqual(summary['success'], 2)
        self.assertEqual(summary['fail'], 1)
        self.assertAlmostEqual(summary['avg_time'], 2.0)

    def test_save_result(self):
        test_results = [
            {"task": "Test Task", "time_taken": 1.23, "success": True, "start_time": 0, "end_time": 1.23}
        ]
        filepath = "data/test_results.csv"
        save_result(test_results, filepath)
        self.assertTrue(os.path.exists(filepath))
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["task"], "Test Task")
        # Cleanup
        os.remove(filepath)

if __name__ == "__main__":
    unittest.main()

