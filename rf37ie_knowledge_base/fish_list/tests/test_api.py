from django.test import TestCase
from fish_list.models import Fish, Bait


class BaitEfficiencyLogicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create minimal test fish with lure data"""
        cls.fish1 = Fish.objects.create(
            id='1001', name='Окунь',
            min_weight=100, max_weight=500,
            min_depth_small=1, min_depth_medium=2, min_depth_large=3,
            amount_on_bottom_small=1, amount_on_bottom_medium=2, amount_on_bottom_large=3,
            amount_on_middle_small=1, amount_on_middle_medium=2, amount_on_middle_large=3,
            amount_on_top_small=1, amount_on_top_medium=2, amount_on_top_large=3,
            filter=1, rating=5, bite_strength=3,
            endurance_small=1, endurance_medium=2, endurance_large=3,
            accuracy_small=1, accuracy_medium=2, accuracy_large=3,
            day_activity_small=1, day_activity_medium=2, day_activity_large=3,
            night_activity_small=1, night_activity_medium=2, night_activity_large=3,
            price=100, rate=10, valuable_weight=300, experience=50, experience_rate=1,
            biting_direction=[], chum_base=[], chum_aromatizer=[],
            lures_small={'червь': 45, 'опарыш': 30},
            lures_medium={'червь': 35, 'кукуруза': 60},
            lures_large={'живец': 80}
        )
        cls.fish2 = Fish.objects.create(
            id='1002', name='Щука',
            min_weight=100, max_weight=500,
            min_depth_small=1, min_depth_medium=2, min_depth_large=3,
            amount_on_bottom_small=1, amount_on_bottom_medium=2, amount_on_bottom_large=3,
            amount_on_middle_small=1, amount_on_middle_medium=2, amount_on_middle_large=3,
            amount_on_top_small=1, amount_on_top_medium=2, amount_on_top_large=3,
            filter=1, rating=5, bite_strength=3,
            endurance_small=1, endurance_medium=2, endurance_large=3,
            accuracy_small=1, accuracy_medium=2, accuracy_large=3,
            day_activity_small=1, day_activity_medium=2, day_activity_large=3,
            night_activity_small=1, night_activity_medium=2, night_activity_large=3,
            price=100, rate=10, valuable_weight=300, experience=50, experience_rate=1,
            biting_direction=[], chum_base=[], chum_aromatizer=[],
            lures_small={'червь': 70, 'мотыль': 90},
            lures_medium={},
            lures_large={}
        )

    def _calculate(self, fish_ids, sizes):
        """Replicate the find_average_bait_efficiency logic from the API"""
        size_to_field = {1: 'lures_small', 2: 'lures_medium', 3: 'lures_large'}
        fish_objects = Fish.objects.filter(id__in=fish_ids)
        fish_map = {fish.id: fish for fish in fish_objects}
        total_fish = len(fish_ids)

        bait_totals = {}
        bait_fish_count = {}

        for fish_id, size in zip(fish_ids, sizes):
            fish = fish_map.get(fish_id)
            if not fish:
                continue
            lures = getattr(fish, size_to_field.get(size, ''), {})
            if not lures:
                continue
            for bait_name, score in lures.items():
                if bait_name not in bait_totals:
                    bait_totals[bait_name] = 0
                    bait_fish_count[bait_name] = 0
                bait_totals[bait_name] += score
                bait_fish_count[bait_name] += 1

        bait_spread = []
        for bait_name in bait_totals:
            avg_score = bait_totals[bait_name] / total_fish
            bait_spread.append({
                'bait_name': bait_name,
                'average_score': round(avg_score, 2),
                'total_score': bait_totals[bait_name],
                'fish_count': bait_fish_count[bait_name],
                'total_fish': total_fish,
            })

        bait_spread.sort(key=lambda x: x['average_score'], reverse=True)
        return bait_spread

    def test_single_fish_small_lures(self):
        """Test one fish, small size"""
        result = self._calculate(['1001'], [1])
        self.assertEqual(len(result), 2)  # червь and опарыш
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        self.assertEqual(cherv['total_score'], 45)
        self.assertEqual(cherv['average_score'], 45.0)
        self.assertEqual(cherv['fish_count'], 1)

    def test_single_fish_medium_lures(self):
        """Test one fish, medium size"""
        result = self._calculate(['1001'], [2])
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        kukur = next(b for b in result if b['bait_name'] == 'кукуруза')
        self.assertEqual(cherv['total_score'], 35)
        self.assertEqual(kukur['total_score'], 60)

    def test_single_fish_large_lures(self):
        """Test one fish, large size"""
        result = self._calculate(['1001'], [3])
        self.assertEqual(len(result), 1)
        zhivets = result[0]
        self.assertEqual(zhivets['bait_name'], 'живец')
        self.assertEqual(zhivets['total_score'], 80)

    def test_two_fish_average(self):
        """Test average across two fish with same bait"""
        result = self._calculate(['1001', '1002'], [1, 1])
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        # червь: 45 (fish1) + 70 (fish2) = 11 / 2 fish = 57.5
        self.assertEqual(cherv['total_score'], 115)
        self.assertEqual(cherv['average_score'], 57.5)
        self.assertEqual(cherv['fish_count'], 2)

    def test_bait_only_on_one_fish(self):
        """Test bait that only exists on one fish - divided by total fish"""
        result = self._calculate(['1001', '1002'], [1, 1])
        oparysh = next(b for b in result if b['bait_name'] == 'опарыш')
        # опарыш: 30 (only fish1) / 2 fish = 15.0
        self.assertEqual(oparysh['total_score'], 30)
        self.assertEqual(oparysh['average_score'], 15.0)
        self.assertEqual(oparysh['fish_count'], 1)

    def test_same_fish_different_sizes(self):
        """Test same fish twice with different sizes"""
        result = self._calculate(['1001', '1001'], [1, 2])
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        # червь: 45 (small) + 35 (medium) = 80 / 2 = 40.0
        self.assertEqual(cherv['total_score'], 80)
        self.assertEqual(cherv['average_score'], 40.0)

    def test_fish_with_no_lures_for_size(self):
        """Test fish that has no lures for the selected size"""
        result = self._calculate(['1002'], [2])
        self.assertEqual(len(result), 0)

    def test_results_sorted_by_score_desc(self):
        """Test that highest score comes first"""
        result = self._calculate(['1001', '1002'], [1, 1])
        scores = [b['average_score'] for b in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_nonexistent_fish_skipped(self):
        """Test that non-existent fish IDs don't break calculation"""
        result = self._calculate(['1001', '9999'], [1, 1])
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        # червь: 45 (fish1 only, 9999 ignored) / 2 total fish = 22.5
        self.assertEqual(cherv['total_score'], 45)
        self.assertEqual(cherv['average_score'], 22.5)

    def test_total_fish_always_includes_all_ids(self):
        """Test that total_fish equals number of IDs, even if some don't exist"""
        result = self._calculate(['1001', '9999', '8888'], [1, 1, 1])
        if result:
            self.assertEqual(result[0]['total_fish'], 3)

    def test_russian_name_lookup(self):
        """Test Bait model lookup for russian name"""
        Bait.objects.create(dev_name='червь', russian_name='Червь навозный')
        result = self._calculate(['1001'], [1])
        cherv = next(b for b in result if b['bait_name'] == 'червь')
        bait_obj = Bait.objects.get(dev_name=cherv['bait_name'])
        self.assertEqual(bait_obj.russian_name, 'Червь навозный')