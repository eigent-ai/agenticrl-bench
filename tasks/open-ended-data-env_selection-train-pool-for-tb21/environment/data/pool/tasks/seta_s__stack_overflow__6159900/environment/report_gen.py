def generate_report(scores_file='leaderboard.txt', report_file='report.txt'):
    scores = []
    with open(scores_file, 'r') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                player, score_str = line.split(':', 1)
                scores.append((player.strip(), int(score_str.strip())))

    if not scores:
        print('No scores found.')
        return

    total = sum(s for _, s in scores)
    avg   = total / len(scores)
    top_player, top_score = max(scores, key=lambda x: x[1])

    with open(report_file, 'w') as f:
        f.write('=== Leaderboard Report ===\n')
        f.write(f'Total Players: {len(scores)}\n')
        f.write(f'Average Score: {avg:.1f}\n')
        f.write(f'Top Player: {top_player} with {top_score}\n')

    print(f'Report saved to {report_file}')


if __name__ == '__main__':
    generate_report()
