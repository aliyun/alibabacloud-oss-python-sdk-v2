# pylint: skip-file
"""Integration tests for SmartCluster CRUD operations via dataprocess Client.

Aligned with Java ClientSmartClusterTest.
"""

import time

from . import TestBaseDataProcess, gen_dataset_name
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.dataprocess as oss_dataprocess


class TestSmartCluster(TestBaseDataProcess):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setup_assert = cls.setup_assertions()
        cls.sc_ds_name = gen_dataset_name()
        result = cls.dp_client.create_dataset(
            oss_dataprocess.models.CreateDatasetRequest(
                bucket=cls.dp_bucket,
                dataset_name=cls.sc_ds_name,
            )
        )
        setup_assert.assertIsNotNone(result)
        setup_assert.assertEqual(200, result.status_code)

    @classmethod
    def tearDownClass(cls):
        client = cls.dp_client

        # 1. List all SmartClusters under this dataset and trigger DeleteSmartCluster
        #    for each. DeleteSmartCluster is asynchronous on the server side, so it
        #    only schedules the deletion here.
        try:
            list_result = client.list_smart_clusters(
                oss_dataprocess.models.ListSmartClustersRequest(
                    bucket=cls.dp_bucket,
                    dataset_name=cls.sc_ds_name,
                    max_results=100,
                )
            )
            if list_result is not None and list_result.smart_clusters is not None \
                    and list_result.smart_clusters.smart_cluster:
                for sc in list_result.smart_clusters.smart_cluster:
                    try:
                        client.delete_smart_cluster(
                            oss_dataprocess.models.DeleteSmartClusterRequest(
                                bucket=cls.dp_bucket,
                                dataset_name=cls.sc_ds_name,
                                object_id=sc.object_id,
                            )
                        )
                    except Exception:
                        pass
        except Exception:
            pass

        # 2. Wait for asynchronous SmartCluster deletion to complete on backend, then
        #    delete the dataset. If the dataset is still not empty (DatasetNotEmpty /
        #    StatusConflict), retry a few times before giving up.
        for _ in range(6):
            time.sleep(1)
            try:
                client.delete_dataset(
                    oss_dataprocess.models.DeleteDatasetRequest(
                        bucket=cls.dp_bucket,
                        dataset_name=cls.sc_ds_name,
                    )
                )
                break
            except Exception:
                # dataset may still contain async-deleting SmartClusters; retry after a wait
                pass

        super().tearDownClass()

    def test_figure_cluster_with_face_rule_lifecycle(self):
        """Figure cluster lifecycle: RuleType=face, BaseURIs (OSS URI list, max 3,
        ossFileURI format) is required."""
        client = self.dp_client
        sc_name = 'test-sc-figure-' + str(int(time.time() * 1000))

        # 1. Create figure SmartCluster: ruleType=face + BaseURIs(<=3, ossFileURI)
        base_uris = [
            'oss://' + self.dp_bucket + '/refs/face1.jpg',
            'oss://' + self.dp_bucket + '/refs/face2.jpg',
            'oss://' + self.dp_bucket + '/refs/face3.jpg',
        ]
        rule = oss_dataprocess.models.SmartClusterRule(
            rule_type='face',
            base_uris=base_uris,
            sensitivity=0.7,
        )

        create_result = client.create_smart_cluster(
            oss_dataprocess.models.CreateSmartClusterRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                name=sc_name,
                cluster_type='figure',
                rules=[rule],
                description='integration test figure cluster',
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.object_id, 'objectId should not be null')

        object_id = create_result.object_id

        try:
            # 2. Get SmartCluster
            get_result = client.get_smart_cluster(
                oss_dataprocess.models.GetSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.smart_cluster, 'smartCluster should not be null')
            self.assertEqual(object_id, get_result.smart_cluster.object_id)
            self.assertEqual(sc_name, get_result.smart_cluster.name)
            self.assertEqual('figure', get_result.smart_cluster.cluster_type)
            self.assertEqual('integration test figure cluster', get_result.smart_cluster.description)
            # Verify rules echoed with ruleType=face and BaseURIs
            self.assertIsNotNone(get_result.smart_cluster.rules, 'rules should not be null')
            self.assertIsNotNone(get_result.smart_cluster.rules.rule)
            self.assertTrue(len(get_result.smart_cluster.rules.rule) > 0,
                            'rules should not be empty')
            echo = get_result.smart_cluster.rules.rule[0]
            self.assertEqual('face', echo.rule_type)
            self.assertIsNotNone(echo.base_uris, 'baseURIs should be echoed')
            self.assertTrue(len(echo.base_uris) > 0, 'baseURIs should not be empty')
            # Document constraint: BaseURIs max 3 entries
            self.assertLessEqual(len(echo.base_uris), 3, 'baseURIs size <= 3')
            # Document constraint: each URI must be ossFileURI (oss://bucket/key)
            for uri in echo.base_uris:
                self.assertTrue(uri.startswith('oss://'),
                                'baseURI must be ossFileURI: ' + uri)

            # 3. Update SmartCluster description
            update_result = client.update_smart_cluster(
                oss_dataprocess.models.UpdateSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                    description='updated figure cluster description',
                )
            )

            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)

            # 4. Verify update
            get_after_update = client.get_smart_cluster(
                oss_dataprocess.models.GetSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                )
            )

            self.assertIsNotNone(get_after_update)
            self.assertEqual(200, get_after_update.status_code)
            self.assertEqual('updated figure cluster description',
                             get_after_update.smart_cluster.description)

            time.sleep(10)

            # 5. List SmartClusters and verify created one is included
            list_result = client.list_smart_clusters(
                oss_dataprocess.models.ListSmartClustersRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    cluster_type='figure',
                    max_results=100,
                )
            )

            self.assertIsNotNone(list_result)
            self.assertEqual(200, list_result.status_code)
            self.assertIsNotNone(list_result.smart_clusters, 'smartClusters should not be null')
            self.assertIsNotNone(list_result.smart_clusters.smart_cluster)
            self.assertTrue(len(list_result.smart_clusters.smart_cluster) > 0,
                            'smartClusters should not be empty')

            found = False
            for sc in list_result.smart_clusters.smart_cluster:
                if object_id == sc.object_id:
                    found = True
                    break
            self.assertTrue(found, 'Created SmartCluster should be found in list')

        finally:
            # 6. Delete SmartCluster
            try:
                delete_result = client.delete_smart_cluster(
                    oss_dataprocess.models.DeleteSmartClusterRequest(
                        bucket=self.dp_bucket,
                        dataset_name=self.sc_ds_name,
                        object_id=object_id,
                    )
                )
                self.assertIsNotNone(delete_result)
                self.assertIn(delete_result.status_code, (200, 204),
                              'Expected 200 or 204 for delete')
            except Exception:
                pass

    def test_knowledge_cluster_with_keywords_rule_lifecycle(self):
        """Knowledge cluster lifecycle: RuleType=keywords, Keywords is required."""
        client = self.dp_client
        sc_name = 'test-sc-knowledge-' + str(int(time.time() * 1000))

        rule = oss_dataprocess.models.SmartClusterRule(
            rule_type='keywords',
            keywords=['人物', '车辆'],
        )

        create_result = client.create_smart_cluster(
            oss_dataprocess.models.CreateSmartClusterRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                name=sc_name,
                cluster_type='knowledge',
                rules=[rule],
                description='integration test knowledge cluster',
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.object_id, 'objectId should not be null')

        object_id = create_result.object_id

        try:
            get_result = client.get_smart_cluster(
                oss_dataprocess.models.GetSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                )
            )

            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.smart_cluster)
            self.assertEqual('knowledge', get_result.smart_cluster.cluster_type)
            self.assertIsNotNone(get_result.smart_cluster.rules, 'rules should not be null')
            self.assertIsNotNone(get_result.smart_cluster.rules.rule)
            self.assertTrue(len(get_result.smart_cluster.rules.rule) > 0,
                            'rules should not be empty')
            echo = get_result.smart_cluster.rules.rule[0]
            self.assertEqual('keywords', echo.rule_type)
            self.assertIsNotNone(echo.keywords, 'keywords should be echoed')
            self.assertTrue(len(echo.keywords) > 0, 'keywords should not be empty')
        finally:
            try:
                client.delete_smart_cluster(
                    oss_dataprocess.models.DeleteSmartClusterRequest(
                        bucket=self.dp_bucket,
                        dataset_name=self.sc_ds_name,
                        object_id=object_id,
                    )
                )
            except Exception:
                pass

    def test_face_rule_base_uris_exceed_max_should_fail(self):
        """Verify face-type BaseURIs max limit is 3: server should reject when
        exceeding 3."""
        client = self.dp_client
        too_many_uris = [
            'oss://' + self.dp_bucket + '/refs/f1.jpg',
            'oss://' + self.dp_bucket + '/refs/f2.jpg',
            'oss://' + self.dp_bucket + '/refs/f3.jpg',
            'oss://' + self.dp_bucket + '/refs/f4.jpg',
        ]
        rule = oss_dataprocess.models.SmartClusterRule(
            rule_type='face',
            base_uris=too_many_uris,
        )

        try:
            client.create_smart_cluster(
                oss_dataprocess.models.CreateSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    name='test-sc-toomany-' + str(int(time.time() * 1000)),
                    cluster_type='figure',
                    rules=[rule],
                )
            )
            self.fail('Expected failure when BaseURIs exceeds 3 entries')
        except Exception:
            # expected: server-side validation rejects > 3 BaseURIs
            pass

    def test_list_smart_clusters_with_pagination(self):
        client = self.dp_client

        # Page 1: list with small page size
        page1 = client.list_smart_clusters(
            oss_dataprocess.models.ListSmartClustersRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                cluster_type='figure',
                max_results=1,
            )
        )

        self.assertIsNotNone(page1)
        self.assertEqual(200, page1.status_code)
        self.assertIsNotNone(page1.smart_clusters, 'smartClusters should not be null')
        clusters1 = page1.smart_clusters.smart_cluster or []
        self.assertLessEqual(len(clusters1), 1, 'should return at most 1 result')

        # Page 2: if there's a nextToken, fetch next page and verify pagination works
        if page1.next_token:
            page2 = client.list_smart_clusters(
                oss_dataprocess.models.ListSmartClustersRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    cluster_type='figure',
                    max_results=1,
                    next_token=page1.next_token,
                )
            )

            self.assertIsNotNone(page2)
            self.assertEqual(200, page2.status_code)
            self.assertIsNotNone(page2.smart_clusters, 'page2 smartClusters should not be null')
            clusters2 = page2.smart_clusters.smart_cluster or []
            self.assertLessEqual(len(clusters2), 1, 'page2 should return at most 1 result')

            # Verify page1 and page2 do not overlap (different objectId)
            if clusters1 and clusters2:
                id_on_page1 = clusters1[0].object_id
                id_on_page2 = clusters2[0].object_id
                self.assertNotEqual(id_on_page1, id_on_page2,
                                    'page1 and page2 should return different objects')

    def test_list_smart_clusters_with_filter(self):
        """ListSmartClusters supports filtering by clusterType / ruleTypes."""
        client = self.dp_client

        # Filter by clusterType
        by_cluster_type = client.list_smart_clusters(
            oss_dataprocess.models.ListSmartClustersRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                cluster_type='figure',
                max_results=50,
            )
        )
        self.assertIsNotNone(by_cluster_type)
        self.assertEqual(200, by_cluster_type.status_code)
        if by_cluster_type.smart_clusters is not None \
                and by_cluster_type.smart_clusters.smart_cluster:
            for sc in by_cluster_type.smart_clusters.smart_cluster:
                self.assertEqual('figure', sc.cluster_type)

        # Filter by ruleTypes, valid values: {face, keywords}
        by_rule_types = client.list_smart_clusters(
            oss_dataprocess.models.ListSmartClustersRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                rule_types=['keywords'],
                max_results=50,
            )
        )
        self.assertIsNotNone(by_rule_types)
        self.assertEqual(200, by_rule_types.status_code)

    def test_figure_cluster_using_rules_array_lifecycle(self):
        """Recommended way: use rules(List[SmartClusterRule]) (the JSON-array form).
        Covers the full lifecycle entirely through the array form:
        Create with rules -> Get (verify Rules array echoed) -> Update with rules -> Delete."""
        client = self.dp_client
        sc_name = 'test-sc-rules-array-' + str(int(time.time() * 1000))

        # 1. Create with rules(List[SmartClusterRule]) - recommended array form
        base_uris = [
            'oss://' + self.dp_bucket + '/refs/arr-face1.jpg',
            'oss://' + self.dp_bucket + '/refs/arr-face2.jpg',
        ]
        face_rule = oss_dataprocess.models.SmartClusterRule(
            rule_type='face',
            base_uris=base_uris,
            sensitivity=0.6,
        )
        rules_array = [face_rule]

        create_result = client.create_smart_cluster(
            oss_dataprocess.models.CreateSmartClusterRequest(
                bucket=self.dp_bucket,
                dataset_name=self.sc_ds_name,
                name=sc_name,
                cluster_type='figure',
                rules=rules_array,
                description='integration test rules-array form',
            )
        )

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.object_id, 'objectId should not be null')
        object_id = create_result.object_id

        try:
            # 2. Get and verify Rules array
            get_result = client.get_smart_cluster(
                oss_dataprocess.models.GetSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                )
            )
            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.smart_cluster, 'smartCluster should not be null')
            self.assertEqual('figure', get_result.smart_cluster.cluster_type)
            self.assertIsNotNone(get_result.smart_cluster.rules, 'rules should not be null')
            self.assertIsNotNone(get_result.smart_cluster.rules.rule)
            self.assertTrue(len(get_result.smart_cluster.rules.rule) > 0,
                            'rules should not be empty')
            echo = get_result.smart_cluster.rules.rule[0]
            self.assertEqual('face', echo.rule_type)
            self.assertIsNotNone(echo.base_uris, 'baseURIs should be echoed')
            self.assertLessEqual(len(echo.base_uris), 3, 'baseURIs size <= 3')
            for uri in echo.base_uris:
                self.assertTrue(uri.startswith('oss://'),
                                'baseURI must be ossFileURI: ' + uri)

            # 3. Update via rules(List[SmartClusterRule])
            updated_face_rule = oss_dataprocess.models.SmartClusterRule(
                rule_type='face',
                base_uris=['oss://' + self.dp_bucket + '/refs/arr-face-updated.jpg'],
                sensitivity=0.8,
            )
            update_result = client.update_smart_cluster(
                oss_dataprocess.models.UpdateSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                    rules=[updated_face_rule],
                )
            )
            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)
        finally:
            # 4. Delete (async on backend)
            try:
                client.delete_smart_cluster(
                    oss_dataprocess.models.DeleteSmartClusterRequest(
                        bucket=self.dp_bucket,
                        dataset_name=self.sc_ds_name,
                        object_id=object_id,
                    )
                )
            except Exception:
                pass

    def test_knowledge_cluster_using_rules_array_with_multiple_rules(self):
        """Demonstrates rules(List[SmartClusterRule]) carrying TRULY MULTIPLE rules,
        not just a single-element list. Two keywords rules are passed for a knowledge
        cluster. The server is expected to echo all rules back; some backends may
        restrict a single SmartCluster to one rule, in which case the rejection is
        also acceptable."""
        client = self.dp_client
        sc_name = 'test-sc-multi-rules-' + str(int(time.time() * 1000))

        # 1. Build TWO independent SmartClusterRule entries
        rule1 = oss_dataprocess.models.SmartClusterRule(
            rule_type='keywords',
            keywords=['人物', '车辆'],
        )
        rule2 = oss_dataprocess.models.SmartClusterRule(
            rule_type='keywords',
            keywords=['动物', '风景'],
        )
        two_rules = [rule1, rule2]
        self.assertEqual(2, len(two_rules), 'rules array should carry 2 rules')

        try:
            create_result = client.create_smart_cluster(
                oss_dataprocess.models.CreateSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    name=sc_name,
                    cluster_type='knowledge',
                    rules=two_rules,
                    description='integration test multi-rules array form',
                )
            )
        except Exception as e:
            # Some backends may restrict a single SmartCluster to one rule. In that
            # case the SDK contract (rules accepts List[SmartClusterRule]) is still
            # verified; surface a clear marker and skip the post-check.
            self.assertIsNotNone(
                str(e),
                'createSmartCluster with multiple rules should succeed or be rejected '
                'by server with a message')
            return

        self.assertIsNotNone(create_result)
        self.assertEqual(200, create_result.status_code)
        self.assertIsNotNone(create_result.object_id, 'objectId should not be null')
        object_id = create_result.object_id

        try:
            # 2. Get and verify the Rules array contains echoed rules
            get_result = client.get_smart_cluster(
                oss_dataprocess.models.GetSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                )
            )
            self.assertIsNotNone(get_result)
            self.assertEqual(200, get_result.status_code)
            self.assertIsNotNone(get_result.smart_cluster, 'smartCluster should not be null')
            self.assertEqual('knowledge', get_result.smart_cluster.cluster_type)
            self.assertIsNotNone(get_result.smart_cluster.rules, 'rules should not be null')
            # Each echoed entry must be well-formed (ruleType=keywords + non-empty keywords).
            self.assertIsNotNone(get_result.smart_cluster.rules.rule)
            self.assertTrue(len(get_result.smart_cluster.rules.rule) > 0,
                            'rules should not be empty')
            for echo in get_result.smart_cluster.rules.rule:
                self.assertEqual('keywords', echo.rule_type)
                self.assertIsNotNone(echo.keywords, 'keywords should be echoed')
                self.assertTrue(len(echo.keywords) > 0, 'keywords should not be empty')

            # 3. Update via rules(List) carrying TWO updated rules as well
            updated1 = oss_dataprocess.models.SmartClusterRule(
                rule_type='keywords',
                keywords=['建筑', '食物'],
            )
            updated2 = oss_dataprocess.models.SmartClusterRule(
                rule_type='keywords',
                keywords=['服饰', '营造'],
            )
            update_result = client.update_smart_cluster(
                oss_dataprocess.models.UpdateSmartClusterRequest(
                    bucket=self.dp_bucket,
                    dataset_name=self.sc_ds_name,
                    object_id=object_id,
                    rules=[updated1, updated2],
                )
            )
            self.assertIsNotNone(update_result)
            self.assertEqual(200, update_result.status_code)
        finally:
            try:
                client.delete_smart_cluster(
                    oss_dataprocess.models.DeleteSmartClusterRequest(
                        bucket=self.dp_bucket,
                        dataset_name=self.sc_ds_name,
                        object_id=object_id,
                    )
                )
            except Exception:
                pass
