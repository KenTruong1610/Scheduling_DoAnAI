# ==========================
#  GREY WOLF OPTIMIZER (GWO)
#  Author: Phước - Nhóm 8, Môn AI
#  Description: Thuật toán tối ưu bầy sói xám (Grey Wolf Optimizer)
#  dùng để giải bài toán Scheduling (phân công N job cho M máy sao cho
#  makespan nhỏ nhất)
#  - Không dùng thư viện ngoài, cài đặt từ đầu
# ==========================

import random
import math
import time
import copy
from typing import List, Tuple, Dict, Any, Union

# ==========================
# 1. Chuẩn hóa dữ liệu job
# ==========================
def _normalize_jobs(jobs):
    """Chuyển danh sách job về dạng [(id, ptime)]"""
    result = []
    if isinstance(jobs[0], dict):
        for j in jobs:
            result.append((j["id"], float(j["p"])))
    else:
        for i, p in enumerate(jobs):
            result.append((i, float(p)))
    return result


# ==========================
# 2. Giải mã vector vị trí -> lịch phân công
# ==========================
def decode_position(position, jobs, m):
    """
    position: vector thực (float)
    jobs: danh sách (id, ptime)
    m: số máy
    Cách làm:
      - Sắp xếp job theo thứ tự position tăng dần (-> thứ tự thực thi)
      - Gán tuần tự job cho máy có tổng thời gian nhỏ nhất
    Trả về: (schedule, makespan)
    """
    normalized = _normalize_jobs(jobs)
    order = sorted(range(len(position)), key=lambda i: position[i])
    loads = [0.0] * m
    schedule = [[] for _ in range(m)]

    for i in order:
        job_id, p = normalized[i]
        # chọn máy rảnh nhất
        min_m = min(range(m), key=lambda x: loads[x])
        schedule[min_m].append(job_id)
        loads[min_m] += p

    makespan = max(loads)
    return schedule, makespan


# ==========================
# 3. GREY WOLF OPTIMIZER
# ==========================
def gwo_schedule(jobs,
                 m,
                 pop_size=30,
                 iters=100,
                 lb=0.0,
                 ub=1.0,
                 seed=None,
                 verbose=False):
    """
    Cài đặt GWO để tối ưu makespan
    jobs: list job (vd: [5,10,3,...]) hoặc [{'id':1,'p':5},...]
    m: số máy
    pop_size: số lượng sói trong đàn
    iters: số vòng lặp
    Trả về:
        best_schedule, best_makespan, info(dict)
    """
    if seed is not None:
        random.seed(seed)

    n_jobs = len(jobs)
    if n_jobs == 0:
        return [], 0.0, {"runtime": 0.0, "best_history": []}

    # Khởi tạo quần thể ngẫu nhiên
    wolves = [[random.uniform(lb, ub) for _ in range(n_jobs)] for _ in range(pop_size)]

    # Hàm fitness: makespan cần minimize
    def fitness(pos):
        _, ms = decode_position(pos, jobs, m)
        return ms

    # Đánh giá ban đầu
    fitness_vals = [fitness(w) for w in wolves]
    idx_sorted = sorted(range(pop_size), key=lambda i: fitness_vals[i])

    alpha = copy.deepcopy(wolves[idx_sorted[0]])
    alpha_score = fitness_vals[idx_sorted[0]]
    beta = copy.deepcopy(wolves[idx_sorted[1]])
    beta_score = fitness_vals[idx_sorted[1]]
    delta = copy.deepcopy(wolves[idx_sorted[2]])
    delta_score = fitness_vals[idx_sorted[2]]

    best_history = [alpha_score]
    start = time.time()

    # --- Vòng lặp chính ---
    for t in range(iters):
        a = 2 - 2 * t / iters  # hệ số giảm tuyến tính (2 → 0)

        for i in range(pop_size):
            X = wolves[i]
            new_X = [0.0] * n_jobs
            for j in range(n_jobs):
                r1, r2 = random.random(), random.random()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[j] - X[j])
                X1 = alpha[j] - A1 * D_alpha

                r1, r2 = random.random(), random.random()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta[j] - X[j])
                X2 = beta[j] - A2 * D_beta

                r1, r2 = random.random(), random.random()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta[j] - X[j])
                X3 = delta[j] - A3 * D_delta

                # Cập nhật vị trí trung bình
                val = (X1 + X2 + X3) / 3.0
                # Giới hạn biên
                val = max(lb, min(ub, val))
                new_X[j] = val

            wolves[i] = new_X

        # Cập nhật alpha, beta, delta
        for i in range(pop_size):
            f = fitness(wolves[i])
            if f < alpha_score:
                delta_score, delta = beta_score, copy.deepcopy(beta)
                beta_score, beta = alpha_score, copy.deepcopy(alpha)
                alpha_score, alpha = f, copy.deepcopy(wolves[i])
            elif f < beta_score:
                delta_score, delta = beta_score, copy.deepcopy(beta)
                beta_score, beta = f, copy.deepcopy(wolves[i])
            elif f < delta_score:
                delta_score, delta = f, copy.deepcopy(wolves[i])

        best_history.append(alpha_score)
        if verbose and (t % max(1, iters // 10) == 0):
            print(f"[GWO] Iter {t}/{iters} - Best makespan: {alpha_score:.4f}")

    runtime = time.time() - start
    best_schedule, best_makespan = decode_position(alpha, jobs, m)
    info = {"runtime": runtime, "best_history": best_history,
            "params": {"pop_size": pop_size, "iters": iters}}
    return best_schedule, best_makespan, info


# ==========================
# 4. Kiểm thử nhanh (chạy độc lập)
# ==========================
if __name__ == "__main__":
    # Sinh 10 job ngẫu nhiên và 3 máy
    random.seed(1)
    jobs = [random.randint(5, 20) for _ in range(10)]
    m = 3

    print("Danh sách job:", jobs)
    schedule, best, info = gwo_schedule(jobs, m, pop_size=25, iters=100, seed=42, verbose=True)

    print("\n--- KẾT QUẢ ---")
    print("Best makespan:", best)
    print("Lịch phân công:", schedule)
    print("Thời gian chạy (s):", round(info["runtime"], 3))
