import torch
import pointops
import numpy as np
from typing import Tuple
import os

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'


def KNNQuery(k: int, coord: torch.Tensor, new_coord: torch.Tensor = None) -> Tuple[torch.Tensor]:
    """
    KNN Indexing

    #! Based on slow or faster than the KDTree implementation, we can keep or remove this function.

    """
    if new_coord is None:
        new_coord = coord
    b, m, _ = new_coord.size()
    n = coord.size(1)

    new_coord_repeat = new_coord.repeat(1, 1, n).view(b, m * n, 3)
    coord_repeat = coord.repeat(1, m, 1).view(b, m * n, 3)
    dist = (new_coord_repeat - coord_repeat).pow(2).sum(dim=2).view(b, m, n)

    [_, idxs] = torch.sort(dist, dim=2)

    # KNNQueryExclude
    #idx = idxs[:, :, 1:k+1].int()
    idx = idxs[:, :, 0:k].int()
    dist = dist[:, :k-1, 0:k].sqrt()

    return idx, dist

# def test_knn():
#     # Test case parameters
#     points = torch.Tensor([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
#     points = torch.stack([points, points], dim=0)

#     query_points = torch.Tensor([[0, 0, 0], [3, 3, 3]])
#     query_points = torch.stack([query_points, query_points], dim=0)

#     offset = torch.Tensor([4, 8])

#     expected_knn_indices = torch.Tensor([
#         [0, 1],
#         [3, 2]
#     ]).long()
#     expected_knn_indices = torch.stack([expected_knn_indices, expected_knn_indices], dim=0)

#     expected_knn_dists = torch.Tensor([
#         [0.0, np.sqrt(3)],
#         [0.0, np.sqrt(3)]
#     ]).float()
#     expected_knn_dists = torch.stack([expected_knn_dists, expected_knn_dists], dim=0)

#     knn_indices, knn_dists = KNNQuery(3, points, query_points)
#     reference_index, _ = pointops.knn_query(3, points, offset, query_points, offset)

#     print("knn_indices:__", "\n", knn_indices, "\n", knn_indices.shape)
#     print("knn_dists:__", "\n", knn_dists, "\n", expected_knn_dists.shape)

#     print("reference_index:__.datatype", "\n", reference_index.dtype)
#     print("reference_index:__.shape", "\n", reference_index.shape)

#     print("reference_index:__", "\n", reference_index.cpu().numpy())
#     print("distances:__", "\n", _.cpu().numpy())

#     np.testing.assert_array_equal(knn_indices.numpy(), expected_knn_indices.numpy())
#     np.testing.assert_array_equal(expected_knn_dists.numpy(), expected_knn_dists.numpy())


#     print("Test passed successfully!")

# # Run the test
# test_knn()



idx = torch.tensor([[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]])

feat = torch.tensor([[0, 0, 0, 10], [1, 1, 1, 10], [2, 2, 2, 10], [3, 3, 3, 10], 
                     [6, 6, 6, 11], [7, 7, 7, 11], [8, 8, 8, 11], [11, 11, 11, 11]])

xyz = torch.randn(2, 10, 3)


knn = KNNQuery(8, xyz)
print("knn:__", "\n", knn, "\n", knn.shape)